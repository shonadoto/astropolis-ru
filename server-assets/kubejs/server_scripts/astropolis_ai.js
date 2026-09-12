// Astropolis pack-aware assistant. The OpenAI key stays in the loopback Python bridge.
const AstropolisAIHttpClient = Java.loadClass('java.net.http.HttpClient')
const AstropolisAIHttpRequest = Java.loadClass('java.net.http.HttpRequest')
const AstropolisAIBodyPublishers = Java.loadClass('java.net.http.HttpRequest$BodyPublishers')
const AstropolisAIBodyHandlers = Java.loadClass('java.net.http.HttpResponse$BodyHandlers')
const AstropolisAIURI = Java.loadClass('java.net.URI')
const AstropolisAIDuration = Java.loadClass('java.time.Duration')
const AstropolisAISystem = Java.loadClass('java.lang.System')

const ASTROPOLIS_AI_PORT = AstropolisAISystem.getenv('AI_BRIDGE_PORT') || '8765'
const ASTROPOLIS_AI_URL = 'http://127.0.0.1:' + ASTROPOLIS_AI_PORT
const ASTROPOLIS_AI_CLIENT = AstropolisAIHttpClient.newBuilder()
  .connectTimeout(AstropolisAIDuration.ofSeconds(2))
  .build()
const ASTROPOLIS_AI_JOBS = {}
const ASTROPOLIS_AI_BUSY = {}
const ASTROPOLIS_AI_PENDING = {}
let astropolisAiTick = 0

function astropolisAiHttp(method, path, payload) {
  let builder = AstropolisAIHttpRequest.newBuilder()
    .uri(AstropolisAIURI.create(ASTROPOLIS_AI_URL + path))
    .timeout(AstropolisAIDuration.ofSeconds(3))
    .header('Accept', 'application/json')
  if (method === 'POST') {
    builder.header('Content-Type', 'application/json; charset=utf-8')
    builder.POST(AstropolisAIBodyPublishers.ofString(JSON.stringify(payload)))
  } else {
    builder.GET()
  }
  let response = ASTROPOLIS_AI_CLIENT.send(
    builder.build(),
    AstropolisAIBodyHandlers.ofString()
  )
  let body = JSON.parse(String(response.body()))
  body.httpStatus = response.statusCode()
  return body
}

function astropolisAiTell(player, message, color) {
  let text = String(message || '').replace(/\s+/g, ' ').trim()
  if (!text) return
  for (let offset = 0; offset < text.length; offset += 240) {
    let part = text.substring(offset, offset + 240)
    let line = color === 'red' ? Component.red(part)
      : color === 'yellow' ? Component.yellow(part)
      : Component.white(part)
    player.tell(Component.aqua('[AI] ').append(line))
  }
}

function astropolisAiPlayerContext(player) {
  let dimension = 'unknown'
  let held = 'minecraft:air'
  try { dimension = String(player.level.dimension) } catch (ignored) {}
  try { held = String(player.mainHandItem.id) } catch (ignored) {}
  return `dimension=${dimension}; position=${Math.floor(player.x)},${Math.floor(player.y)},${Math.floor(player.z)}; health=${player.health}; held=${held}`
}

function astropolisAiSafeCommand(command, playerName) {
  let value = String(command || '').trim().replace(/^\//, '')
  if (!value || value.length > 180 || /[\r\n;|&]/.test(value)) return false
  let escaped = String(playerName).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  let id = '[a-z0-9_.-]+:[a-z0-9_./-]+'
  let number = '-?(?:\\d+(?:\\.\\d+)?|\\.\\d+)'
  let patterns = [
    new RegExp(`^give ${escaped} ${id}(?: \\d+)?$`, 'i'),
    new RegExp(`^effect (?:give|clear) ${escaped}(?: ${id})?(?: \\d+)?(?: \\d+)?(?: (?:true|false))?$`, 'i'),
    new RegExp(`^gamemode (?:survival|creative|adventure|spectator) ${escaped}$`, 'i'),
    new RegExp(`^tp ${escaped} ${number} ${number} ${number}(?: ${number} ${number})?$`, 'i'),
    new RegExp(`^clear ${escaped}(?: ${id})?(?: \\d+)?$`, 'i'),
    new RegExp(`^kill ${escaped}$`, 'i'),
    new RegExp(`^spawnpoint ${escaped}(?: ${number} ${number} ${number}(?: ${number})?)?$`, 'i'),
    /^time set (?:day|night|noon|midnight|\d+)$/i,
    /^weather (?:clear|rain|thunder)(?: \d+)?$/i,
    /^difficulty (?:peaceful|easy|normal|hard)$/i,
    /^gamerule (?:keepInventory|doDaylightCycle|doWeatherCycle|mobGriefing) (?:true|false)$/i,
    new RegExp(`^setworldspawn(?: ${number} ${number} ${number}(?: ${number})?)?$`, 'i')
  ]
  return patterns.some(pattern => pattern.test(value))
}

function astropolisAiAsk(ctx, message) {
  let player = ctx.source.player
  if (!player) return 0
  let name = String(player.username)
  let key = name.toLowerCase()
  if (ASTROPOLIS_AI_BUSY[key]) {
    astropolisAiTell(player, 'Предыдущий запрос ещё обрабатывается.', 'yellow')
    return 0
  }
  try {
    let response = astropolisAiHttp('POST', '/ask', {
      player: name,
      message: String(message),
      context: astropolisAiPlayerContext(player)
    })
    if (!response.ok || !response.job_id) {
      astropolisAiTell(player, response.error || 'Мост отклонил запрос.', 'red')
      return 0
    }
    let jobId = String(response.job_id)
    ASTROPOLIS_AI_BUSY[key] = true
    ASTROPOLIS_AI_JOBS[jobId] = { player: name, key: key, started: Date.now() }
    astropolisAiTell(player, 'Думаю…', 'yellow')
    return 1
  } catch (error) {
    astropolisAiTell(player, 'AI-мост недоступен. Проверь ./serverctl ai-status.', 'red')
    console.error(`[Astropolis AI] request failed: ${error}`)
    return 0
  }
}

function astropolisAiConfirm(ctx) {
  let player = ctx.source.player
  if (!player) return 0
  let name = String(player.username)
  let key = name.toLowerCase()
  let pending = ASTROPOLIS_AI_PENDING[key]
  if (!pending || pending.expires < Date.now()) {
    delete ASTROPOLIS_AI_PENDING[key]
    astropolisAiTell(player, 'Нет команды, ожидающей подтверждения.', 'yellow')
    return 0
  }
  delete ASTROPOLIS_AI_PENDING[key]
  let completed = 0
  pending.commands.forEach(entry => {
    let command = String(entry.command || '').replace(/^\//, '')
    if (!astropolisAiSafeCommand(command, name)) {
      console.error(`[Astropolis AI] blocked command at execution: ${command}`)
      astropolisAiTell(player, `Команда заблокирована фильтром: /${command}`, 'red')
      return
    }
    player.server.runCommandSilent(command)
    completed++
  })
  astropolisAiTell(player, `Выполнено команд: ${completed}.`, completed ? 'white' : 'red')
  return completed ? 1 : 0
}

function astropolisAiCancel(ctx) {
  let player = ctx.source.player
  if (!player) return 0
  let key = String(player.username).toLowerCase()
  if (ASTROPOLIS_AI_PENDING[key]) {
    delete ASTROPOLIS_AI_PENDING[key]
    astropolisAiTell(player, 'Предложенные команды отменены.', 'yellow')
    return 1
  }
  astropolisAiTell(player, 'Отменять нечего.', 'yellow')
  return 0
}

ServerEvents.commandRegistry(event => {
  const { commands: Commands, arguments: Arguments } = event
  event.register(
    Commands.literal('ai')
      .executes(ctx => {
        let player = ctx.source.player
        if (player) astropolisAiTell(player, 'Использование: /ai <вопрос>, /ai confirm, /ai cancel')
        return 1
      })
      .then(Commands.literal('confirm').executes(ctx => astropolisAiConfirm(ctx)))
      .then(Commands.literal('cancel').executes(ctx => astropolisAiCancel(ctx)))
      .then(
        Commands.argument('message', Arguments.GREEDY_STRING.create(event))
          .executes(ctx => astropolisAiAsk(ctx, Arguments.GREEDY_STRING.getResult(ctx, 'message')))
      )
  )
})

ServerEvents.tick(event => {
  astropolisAiTick++
  if (astropolisAiTick % 20 !== 0) return
  Object.keys(ASTROPOLIS_AI_JOBS).forEach(jobId => {
    let job = ASTROPOLIS_AI_JOBS[jobId]
    if (Date.now() - job.started > 120000) {
      delete ASTROPOLIS_AI_JOBS[jobId]
      delete ASTROPOLIS_AI_BUSY[job.key]
      let timedOutPlayer = event.server.getPlayer(job.player)
      if (timedOutPlayer) astropolisAiTell(timedOutPlayer, 'Ответ не пришёл за 2 минуты, запрос отменён.', 'red')
      return
    }
    try {
      let result = astropolisAiHttp('GET', '/result/' + jobId, null)
      if (result.pending) return
      delete ASTROPOLIS_AI_JOBS[jobId]
      delete ASTROPOLIS_AI_BUSY[job.key]
      let player = event.server.getPlayer(job.player)
      if (!player) return
      if (!result.ok) {
        astropolisAiTell(player, result.error || 'Не удалось получить ответ.', 'red')
        return
      }
      astropolisAiTell(player, result.reply || 'Готово.')
      let commands = Array.isArray(result.commands) ? result.commands : []
      commands = commands.filter(entry => astropolisAiSafeCommand(entry.command, job.player))
      if (commands.length) {
        ASTROPOLIS_AI_PENDING[job.key] = {
          commands: commands,
          expires: Date.now() + 60000
        }
        commands.forEach(entry => {
          astropolisAiTell(player, `Предлагаю: /${entry.command}${entry.reason ? ' — ' + entry.reason : ''}`, 'yellow')
        })
        astropolisAiTell(player, 'Выполнить: /ai confirm. Отмена: /ai cancel. Срок — 60 секунд.', 'yellow')
      }
    } catch (error) {
      delete ASTROPOLIS_AI_JOBS[jobId]
      delete ASTROPOLIS_AI_BUSY[job.key]
      let player = event.server.getPlayer(job.player)
      if (player) astropolisAiTell(player, 'Связь с AI-мостом потеряна.', 'red')
      console.error(`[Astropolis AI] polling failed: ${error}`)
    }
  })
})
