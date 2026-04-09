const apiTokenInput = document.getElementById('apiToken');
const commandInput = document.getElementById('commandInput');
const browserUrlInput = document.getElementById('browserUrlInput');
const sendBtn = document.getElementById('sendBtn');
const openUrlBtn = document.getElementById('openUrlBtn');
const taskIdEl = document.getElementById('taskId');
const taskStatusEl = document.getElementById('taskStatus');
const resultBox = document.getElementById('resultBox');
const cancelBtn = document.getElementById('cancelBtn');
const mediaUploadInput = document.getElementById('mediaUploadInput');
const mediaUploadBtn = document.getElementById('mediaUploadBtn');
const mediaStatus = document.getElementById('mediaStatus');
const mediaGrid = document.getElementById('mediaGrid');
const mediaPreviewMount = document.getElementById('mediaPreviewMount');
const mediaPreviewEmpty = document.getElementById('mediaPreviewEmpty');
const favoriteTitleInput = document.getElementById('favoriteTitleInput');
const favoriteUrlInput = document.getElementById('favoriteUrlInput');
const favoriteAddBtn = document.getElementById('favoriteAddBtn');
const favoriteStatus = document.getElementById('favoriteStatus');
const favoriteList = document.getElementById('favoriteList');
const tvTextInput = document.getElementById('tvTextInput');
const tvTextSendBtn = document.getElementById('tvTextSendBtn');
const tvPowerOnBtn = document.getElementById('tvPowerOnBtn');
const tvWakeScreenBtn = document.getElementById('tvWakeScreenBtn');
const tvPowerOffBtn = document.getElementById('tvPowerOffBtn');
const powerDelayInput = document.getElementById('powerDelayInput');
const schedulePowerBtn = document.getElementById('schedulePowerBtn');
const powerStatus = document.getElementById('powerStatus');
const powerScheduleList = document.getElementById('powerScheduleList');
const reminderTitleInput = document.getElementById('reminderTitleInput');
const reminderNoteInput = document.getElementById('reminderNoteInput');
const reminderAtInput = document.getElementById('reminderAtInput');
const reminderPowerOnInput = document.getElementById('reminderPowerOnInput');
const reminderWakeInput = document.getElementById('reminderWakeInput');
const reminderAddBtn = document.getElementById('reminderAddBtn');
const reminderStatus = document.getElementById('reminderStatus');
const reminderList = document.getElementById('reminderList');
const weatherLabel = document.getElementById('weatherLabel');
const weatherTemp = document.getElementById('weatherTemp');
const weatherDesc = document.getElementById('weatherDesc');
const weatherHumidity = document.getElementById('weatherHumidity');
const weatherWind = document.getElementById('weatherWind');
const weatherTime = document.getElementById('weatherTime');
const newsOverlayBtn = document.getElementById('newsOverlayBtn');
const newsSource = document.getElementById('newsSource');
const newsUpdatedAt = document.getElementById('newsUpdatedAt');
const newsList = document.getElementById('newsList');
const newsOverlay = document.getElementById('newsOverlay');
const newsOverlayTitle = document.getElementById('newsOverlayTitle');
const newsOverlayUpdatedAt = document.getElementById('newsOverlayUpdatedAt');
const newsOverlayList = document.getElementById('newsOverlayList');
const newsOverlayCloseBtn = document.getElementById('newsOverlayCloseBtn');
const standbyBtn = document.getElementById('standbyBtn');
const standbyOverlay = document.getElementById('standbyOverlay');
const closeStandbyBtn = document.getElementById('closeStandbyBtn');
const standbyClock = document.getElementById('standbyClock');
const standbyWeatherLabel = document.getElementById('standbyWeatherLabel');
const standbyWeatherTemp = document.getElementById('standbyWeatherTemp');
const standbyWeatherDesc = document.getElementById('standbyWeatherDesc');
const standbyWeatherHumidity = document.getElementById('standbyWeatherHumidity');
const standbyWeatherWind = document.getElementById('standbyWeatherWind');
const standbyWeatherTime = document.getElementById('standbyWeatherTime');
const reminderOverlay = document.getElementById('reminderOverlay');
const reminderOverlayTitle = document.getElementById('reminderOverlayTitle');
const reminderOverlayNote = document.getElementById('reminderOverlayNote');
const reminderOverlayTime = document.getElementById('reminderOverlayTime');
const reminderOverlayCloseBtn = document.getElementById('reminderOverlayCloseBtn');
const whiteboardCanvas = document.getElementById('whiteboardCanvas');
const penColorInput = document.getElementById('penColor');
const penSizeInput = document.getElementById('penSize');
const clearBoardBtn = document.getElementById('clearBoardBtn');

const whiteboardCtx = whiteboardCanvas.getContext('2d');
const whiteboardClientId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random());

let pollHandle = null;
let whiteboardSocket = null;
let whiteboardReconnectHandle = null;
let whiteboardReady = false;
const whiteboardStrokes = new Map();
const whiteboardOrder = [];
let activeStrokeId = null;
let activeStroke = null;
let weatherState = null;
let mediaState = { uploads: [], favorites: [] };
let reminderState = [];
let newsState = null;
let currentPreviewType = 'none';
let reminderSocket = null;
let reminderReconnectHandle = null;
let activeReminder = null;

function setStatus(status, result) {
  taskStatusEl.textContent = status;
  if (result) {
    resultBox.textContent = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
  }
}

function apiHeaders(token, extra = {}) {
  return {
    ...extra,
    'X-API-Token': token,
  };
}

function showMediaPreview(element) {
  mediaPreviewMount.innerHTML = '';
  mediaPreviewMount.appendChild(element);
  mediaPreviewEmpty.style.display = 'none';
}

function resetMediaPreview() {
  mediaPreviewMount.innerHTML = '';
  mediaPreviewEmpty.style.display = 'block';
  currentPreviewType = 'none';
}

function renderMediaPreviewForItem(item) {
  if (!item) {
    resetMediaPreview();
    return;
  }
  let node;
  if (item.kind === 'video') {
    node = document.createElement('video');
    node.controls = true;
    node.autoplay = false;
    node.src = item.url;
  } else if (item.kind === 'audio') {
    node = document.createElement('audio');
    node.controls = true;
    node.autoplay = false;
    node.src = item.url;
  } else if (item.kind === 'image') {
    node = document.createElement('img');
    node.src = item.url;
    node.alt = item.original_name;
  } else {
    node = document.createElement('a');
    node.href = item.url;
    node.target = '_blank';
    node.rel = 'noreferrer';
    node.textContent = item.original_name;
  }
  currentPreviewType = item.kind;
  showMediaPreview(node);
}

function youtubeEmbedUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes('youtu.be')) {
      const id = parsed.pathname.replace('/', '');
      return `https://www.youtube.com/embed/${id}`;
    }
    if (parsed.hostname.includes('youtube.com')) {
      const id = parsed.searchParams.get('v');
      if (id) return `https://www.youtube.com/embed/${id}`;
    }
  } catch {
    return url;
  }
  return url;
}

function renderFavoritePreview(link) {
  const iframe = document.createElement('iframe');
  iframe.src = youtubeEmbedUrl(link.url);
  iframe.allow = 'autoplay; encrypted-media; picture-in-picture';
  iframe.allowFullscreen = true;
  iframe.title = link.title;
  currentPreviewType = 'favorite';
  showMediaPreview(iframe);
}

function renderMediaGrid() {
  mediaGrid.innerHTML = '';
  if (!mediaState.uploads.length) {
    mediaGrid.innerHTML = '<div class="fineprint">업로드된 파일이 없습니다.</div>';
    return;
  }
  for (const item of mediaState.uploads) {
    const card = document.createElement('div');
    card.className = 'media-item';
    card.innerHTML = `
      <strong>${item.original_name}</strong>
      <div class="meta">${item.kind} · ${(item.size_bytes / 1024 / 1024).toFixed(2)} MB</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const openBtn = document.createElement('button');
    openBtn.type = 'button';
    openBtn.textContent = '재생';
    openBtn.addEventListener('click', () => renderMediaPreviewForItem(item));
    const linkBtn = document.createElement('button');
    linkBtn.type = 'button';
    linkBtn.textContent = '링크 복사';
    linkBtn.addEventListener('click', async () => {
      await navigator.clipboard.writeText(`${window.location.origin}${item.url}`);
      mediaStatus.textContent = '미디어 링크를 복사했습니다.';
    });
    actions.append(openBtn, linkBtn);
    card.append(actions);
    mediaGrid.appendChild(card);
  }
}

function renderFavoriteList() {
  favoriteList.innerHTML = '';
  if (!mediaState.favorites.length) {
    favoriteList.innerHTML = '<div class="fineprint">저장된 링크가 없습니다.</div>';
    return;
  }
  for (const link of mediaState.favorites) {
    const card = document.createElement('div');
    card.className = 'favorite-item';
    card.innerHTML = `
      <strong>${link.title}</strong>
      <div class="meta">${link.url}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const playBtn = document.createElement('button');
    playBtn.type = 'button';
    playBtn.textContent = '재생';
    playBtn.addEventListener('click', () => renderFavoritePreview(link));
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/favorites/videos/${link.favorite_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        favoriteStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      favoriteStatus.textContent = '삭제했습니다.';
      await loadMediaLibrary();
    });
    actions.append(playBtn, deleteBtn);
    card.append(actions);
    favoriteList.appendChild(card);
  }
}

function renderPowerSchedules(schedules) {
  powerScheduleList.innerHTML = '';
  if (!schedules.length) {
    powerScheduleList.innerHTML = '<div class="fineprint">예약된 전원 끄기가 없습니다.</div>';
    return;
  }
  for (const schedule of schedules) {
    const card = document.createElement('div');
    card.className = 'schedule-item';
    card.innerHTML = `
      <strong>${schedule.minutes}분 뒤 전원 끄기</strong>
      <div class="meta">${schedule.due_at}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const cancelBtnEl = document.createElement('button');
    cancelBtnEl.type = 'button';
    cancelBtnEl.textContent = '취소';
    cancelBtnEl.addEventListener('click', async () => {
      const res = await fetch(`/tv/power/schedule/${schedule.timer_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        powerStatus.textContent = data.detail || '취소 실패';
        return;
      }
      powerStatus.textContent = '예약을 취소했습니다.';
      await loadPowerSchedules();
    });
    actions.append(cancelBtnEl);
    card.append(actions);
    powerScheduleList.appendChild(card);
  }
}

function formatDateTimeLocalOffset(date) {
  const pad = (value) => String(value).padStart(2, '0');
  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function formatReminderTime(value) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function showReminderOverlay(reminder) {
  activeReminder = reminder;
  reminderOverlayTitle.textContent = reminder.title || '알림';
  reminderOverlayNote.textContent = reminder.note || '메모 없음';
  reminderOverlayTime.textContent = `예정 시각 ${formatReminderTime(reminder.due_at)}`;
  reminderOverlay.classList.remove('hidden');
}

function hideReminderOverlay() {
  activeReminder = null;
  reminderOverlay.classList.add('hidden');
}

function renderReminders(reminders) {
  reminderList.innerHTML = '';
  if (!reminders.length) {
    reminderList.innerHTML = '<div class="fineprint">등록된 스케줄 알림이 없습니다.</div>';
    return;
  }
  for (const reminder of reminders) {
    const card = document.createElement('div');
    card.className = 'reminder-item';
    card.innerHTML = `
      <strong>${reminder.title}</strong>
      <div class="meta">${formatReminderTime(reminder.due_at)} · ${reminder.status}</div>
      <div class="meta">${reminder.note || '메모 없음'}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/reminders/${reminder.reminder_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        reminderStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      reminderStatus.textContent = '삭제했습니다.';
      await loadReminders();
    });
    actions.append(deleteBtn);
    card.append(actions);
    reminderList.appendChild(card);
  }
}

function renderNewsList(items, mount) {
  mount.innerHTML = '';
  if (!items.length) {
    mount.innerHTML = '<div class="fineprint">헤드라인이 없습니다.</div>';
    return;
  }
  for (const item of items) {
    const card = document.createElement('a');
    card.className = 'news-item';
    card.href = item.link;
    card.target = '_blank';
    card.rel = 'noreferrer';
    card.innerHTML = `
      <strong>${item.title}</strong>
      <div class="meta">${item.published_at || '발행 시각 정보 없음'}</div>
      <div class="news-summary">${item.summary || ''}</div>
    `;
    mount.appendChild(card);
  }
}

function updateWeatherDisplay(weather) {
  if (!weather) return;
  weatherLabel.textContent = weather.label || '-';
  weatherTemp.textContent = weather.temperature_c == null ? '--°' : `${Math.round(weather.temperature_c)}°`;
  weatherDesc.textContent = weather.description || '-';
  weatherHumidity.textContent = weather.humidity == null ? '습도 --%' : `습도 ${weather.humidity}%`;
  weatherWind.textContent = weather.wind_speed == null ? '풍속 --m/s' : `풍속 ${weather.wind_speed}m/s`;
  weatherTime.textContent = weather.observation_time ? `기준 시각 ${weather.observation_time}` : '기준 시각 --';

  standbyWeatherLabel.textContent = weather.label || '-';
  standbyWeatherTemp.textContent = weather.temperature_c == null ? '--°' : `${Math.round(weather.temperature_c)}°`;
  standbyWeatherDesc.textContent = weather.description || '-';
  standbyWeatherHumidity.textContent = weather.humidity == null ? '습도 --%' : `습도 ${weather.humidity}%`;
  standbyWeatherWind.textContent = weather.wind_speed == null ? '풍속 --m/s' : `풍속 ${weather.wind_speed}m/s`;
  standbyWeatherTime.textContent = weather.observation_time ? `기준 시각 ${weather.observation_time}` : '기준 시각 --';
}

async function loadWeather() {
  try {
    const res = await fetch('/weather/current');
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'weather load failed');
    }
    weatherState = data;
    updateWeatherDisplay(data);
  } catch (err) {
    const message = `날씨를 불러올 수 없습니다: ${err}`;
    weatherDesc.textContent = message;
    standbyWeatherDesc.textContent = message;
  }
}

async function loadNews() {
  try {
    const res = await fetch('/news/yonhap');
    const data = await res.json();
    if (!res.ok) {
      newsSource.textContent = data.detail || '연합뉴스 피드를 불러오지 못했습니다.';
      return;
    }
    newsState = data;
    newsSource.textContent = data.title || '연합뉴스';
    newsUpdatedAt.textContent = data.updated_at ? `업데이트 ${data.updated_at}` : '업데이트 정보 없음';
    renderNewsList(data.items || [], newsList);
    newsOverlayTitle.textContent = data.title || '헤드라인';
    newsOverlayUpdatedAt.textContent = data.updated_at ? `업데이트 ${data.updated_at}` : '업데이트 정보 없음';
    renderNewsList(data.items || [], newsOverlayList);
  } catch (err) {
    const message = `연합뉴스 피드를 불러올 수 없습니다: ${err}`;
    newsSource.textContent = message;
    newsUpdatedAt.textContent = '업데이트 실패';
  }
}

async function loadMediaLibrary() {
  try {
    const res = await fetch('/media/library');
    const data = await res.json();
    if (!res.ok) {
      mediaStatus.textContent = data.detail || '미디어 목록을 불러오지 못했습니다.';
      return;
    }
    mediaState = data;
    renderMediaGrid();
    renderFavoriteList();
  } catch (err) {
    mediaStatus.textContent = `미디어 목록 오류: ${err}`;
  }
}

async function loadPowerSchedules() {
  try {
    const res = await fetch('/tv/power/schedule');
    const data = await res.json();
    if (!res.ok) {
      powerStatus.textContent = data.detail || '예약 목록을 불러오지 못했습니다.';
      return;
    }
    renderPowerSchedules(data);
  } catch (err) {
    powerStatus.textContent = `예약 목록 오류: ${err}`;
  }
}

async function loadReminders() {
  try {
    const res = await fetch('/reminders');
    const data = await res.json();
    if (!res.ok) {
      reminderStatus.textContent = data.detail || '알림 목록을 불러오지 못했습니다.';
      return;
    }
    reminderState = data;
    renderReminders(data);
  } catch (err) {
    reminderStatus.textContent = `알림 목록 오류: ${err}`;
  }
}

async function uploadSelectedFiles() {
  const token = apiTokenInput.value.trim();
  const files = Array.from(mediaUploadInput.files || []);
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!files.length) {
    mediaStatus.textContent = '업로드할 파일을 선택하세요.';
    return;
  }

  mediaStatus.textContent = '업로드 중...';
  for (const file of files) {
    const dataBase64 = await readFileAsBase64(file);
    const res = await fetch('/media/upload', {
      method: 'POST',
      headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        filename: file.name,
        content_type: file.type || 'application/octet-stream',
        data_base64: dataBase64,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      mediaStatus.textContent = data.detail || `업로드 실패: ${file.name}`;
      return;
    }
  }
  mediaStatus.textContent = '업로드를 완료했습니다.';
  mediaUploadInput.value = '';
  await loadMediaLibrary();
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const value = String(reader.result || '');
      resolve(value.includes(',') ? value.split(',')[1] : value);
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

async function addFavoriteVideo() {
  const token = apiTokenInput.value.trim();
  const title = favoriteTitleInput.value.trim();
  const url = favoriteUrlInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!title || !url) {
    favoriteStatus.textContent = '제목과 URL을 모두 입력하세요.';
    return;
  }
  const res = await fetch('/favorites/videos', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ title, url }),
  });
  const data = await res.json();
  if (!res.ok) {
    favoriteStatus.textContent = data.detail || '저장 실패';
    return;
  }
  favoriteStatus.textContent = '저장했습니다.';
  favoriteTitleInput.value = '';
  favoriteUrlInput.value = '';
  await loadMediaLibrary();
}

async function sendTextToTv() {
  const token = apiTokenInput.value.trim();
  const text = tvTextInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!text) {
    powerStatus.textContent = '보낼 글자를 입력하세요.';
    return;
  }
  const res = await fetch('/tv/text', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ text }),
  });
  const data = await res.json();
  if (!res.ok) {
    powerStatus.textContent = data.detail || '글자 전송 실패';
    return;
  }
  tvTextInput.value = '';
  powerStatus.textContent = '글자를 전송했습니다.';
  taskIdEl.textContent = data.task_id;
  setStatus('pending', '글자 전송 작업이 등록되었습니다.');
  pollTask(data.task_id, token);
}

async function powerOffNow() {
  const token = apiTokenInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  const res = await fetch('/tv/power/off', {
    method: 'POST',
    headers: apiHeaders(token),
  });
  const data = await res.json();
  if (!res.ok) {
    powerStatus.textContent = data.detail || '전원 끄기 실패';
    return;
  }
  powerStatus.textContent = data.message || '전원을 껐습니다.';
}

async function powerOnNow() {
  const token = apiTokenInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  const res = await fetch('/tv/power/on', {
    method: 'POST',
    headers: apiHeaders(token),
  });
  const data = await res.json();
  if (!res.ok) {
    powerStatus.textContent = data.detail || '전원 켜기 실패';
    return;
  }
  powerStatus.textContent = data.message || '전원을 켰습니다.';
}

async function wakeScreenNow() {
  const token = apiTokenInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  const res = await fetch('/tv/screen/wake', {
    method: 'POST',
    headers: apiHeaders(token),
  });
  const data = await res.json();
  if (!res.ok) {
    powerStatus.textContent = data.detail || '화면 깨우기 실패';
    return;
  }
  powerStatus.textContent = data.message || '화면을 깨웠습니다.';
}

async function schedulePowerOff() {
  const token = apiTokenInput.value.trim();
  const minutes = Number(powerDelayInput.value);
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!Number.isFinite(minutes) || minutes < 1) {
    powerStatus.textContent = '분 수를 올바르게 입력하세요.';
    return;
  }
  const res = await fetch('/tv/power/schedule', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ minutes }),
  });
  const data = await res.json();
  if (!res.ok) {
    powerStatus.textContent = data.detail || '예약 실패';
    return;
  }
  powerStatus.textContent = `${data.minutes}분 뒤 전원을 끄도록 예약했습니다.`;
  await loadPowerSchedules();
}

async function scheduleReminder() {
  const token = apiTokenInput.value.trim();
  const title = reminderTitleInput.value.trim();
  const note = reminderNoteInput.value.trim();
  const dueAt = reminderAtInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!title || !dueAt) {
    reminderStatus.textContent = '제목과 시간은 필수입니다.';
    return;
  }
  const res = await fetch('/reminders', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({
      title,
      note,
      due_at: dueAt,
      power_on: reminderPowerOnInput.checked,
      wake_screen: reminderWakeInput.checked,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    reminderStatus.textContent = data.detail || '알림 예약 실패';
    return;
  }
  reminderStatus.textContent = `${data.title} 알림을 예약했습니다.`;
  reminderTitleInput.value = '';
  reminderNoteInput.value = '';
  await loadReminders();
}

function updateStandbyClock() {
  const now = new Date();
  standbyClock.textContent = now.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function openStandby() {
  standbyOverlay.classList.remove('hidden');
  updateStandbyClock();
  if (weatherState) {
    updateWeatherDisplay(weatherState);
  }
}

function closeStandby() {
  standbyOverlay.classList.add('hidden');
}

function openNewsOverlay() {
  newsOverlay.classList.remove('hidden');
  if (newsState) {
    newsOverlayTitle.textContent = newsState.title || '헤드라인';
    newsOverlayUpdatedAt.textContent = newsState.updated_at ? `업데이트 ${newsState.updated_at}` : '업데이트 정보 없음';
    renderNewsList(newsState.items || [], newsOverlayList);
  }
}

function closeNewsOverlay() {
  newsOverlay.classList.add('hidden');
}

function connectReminders() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  reminderSocket = new WebSocket(`${protocol}//${window.location.host}/ws/reminders`);
  reminderSocket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'snapshot') {
      reminderState = data.reminders || [];
      renderReminders(reminderState);
    }
    if (data.type === 'reminder-fired' && data.reminder) {
      reminderState = reminderState
        .filter((item) => item.reminder_id !== data.reminder.reminder_id)
        .concat([data.reminder]);
      renderReminders(reminderState);
      showReminderOverlay(data.reminder);
      reminderStatus.textContent = `${data.reminder.title} 알림 시간이 되었습니다.`;
    }
  });
  reminderSocket.addEventListener('close', () => {
    if (reminderReconnectHandle) clearTimeout(reminderReconnectHandle);
    reminderReconnectHandle = setTimeout(connectReminders, 1000);
  });
}

function resizeWhiteboardCanvas() {
  const rect = whiteboardCanvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  whiteboardCanvas.width = Math.max(1, Math.floor(rect.width * dpr));
  whiteboardCanvas.height = Math.max(1, Math.floor(rect.height * dpr));
  whiteboardCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  redrawWhiteboard();
}

function clearWhiteboardLocal() {
  whiteboardStrokes.clear();
  whiteboardOrder.length = 0;
  redrawWhiteboard();
}

function redrawWhiteboard() {
  const width = whiteboardCanvas.getBoundingClientRect().width;
  const height = whiteboardCanvas.getBoundingClientRect().height;
  whiteboardCtx.clearRect(0, 0, width, height);
  for (const strokeId of whiteboardOrder) {
    drawStroke(whiteboardStrokes.get(strokeId));
  }
}

function drawStroke(stroke) {
  if (!stroke || !stroke.points || stroke.points.length === 0) return;

  whiteboardCtx.save();
  whiteboardCtx.strokeStyle = stroke.color || '#7dd3fc';
  whiteboardCtx.fillStyle = stroke.color || '#7dd3fc';
  whiteboardCtx.lineWidth = Number(stroke.size || 4);
  whiteboardCtx.lineJoin = 'round';
  whiteboardCtx.lineCap = 'round';

  const points = stroke.points;
  if (points.length === 1) {
    const point = points[0];
    whiteboardCtx.beginPath();
    whiteboardCtx.arc(point.x, point.y, Math.max(1, whiteboardCtx.lineWidth / 2), 0, Math.PI * 2);
    whiteboardCtx.fill();
  } else {
    whiteboardCtx.beginPath();
    whiteboardCtx.moveTo(points[0].x, points[0].y);
    for (const point of points.slice(1)) {
      whiteboardCtx.lineTo(point.x, point.y);
    }
    whiteboardCtx.stroke();
  }

  whiteboardCtx.restore();
}

function normalizePoint(event) {
  const rect = whiteboardCanvas.getBoundingClientRect();
  return {
    x: Math.max(0, Math.min(rect.width, event.clientX - rect.left)),
    y: Math.max(0, Math.min(rect.height, event.clientY - rect.top)),
  };
}

function applyStrokePoints(strokeId, points, color, size, tool = 'pen') {
  let stroke = whiteboardStrokes.get(strokeId);
  if (!stroke) {
    stroke = { id: strokeId, points: [], color, size, tool };
    whiteboardStrokes.set(strokeId, stroke);
    whiteboardOrder.push(strokeId);
  }
  stroke.color = color || stroke.color;
  stroke.size = size || stroke.size;
  stroke.tool = tool || stroke.tool;
  stroke.points.push(...points);
  redrawWhiteboard();
}

function sendWhiteboardEvent(payload) {
  if (whiteboardSocket && whiteboardSocket.readyState === WebSocket.OPEN) {
    whiteboardSocket.send(JSON.stringify(payload));
  }
}

function connectWhiteboard() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  whiteboardSocket = new WebSocket(`${protocol}//${window.location.host}/ws/whiteboard`);
  whiteboardSocket.addEventListener('open', () => {
    whiteboardReady = true;
  });
  whiteboardSocket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.clientId && data.clientId === whiteboardClientId) {
      return;
    }
    if (data.type === 'snapshot') {
      clearWhiteboardLocal();
      for (const stroke of data.strokes || []) {
        whiteboardStrokes.set(stroke.id, stroke);
        whiteboardOrder.push(stroke.id);
      }
      redrawWhiteboard();
    }
    if (data.type === 'stroke-point') {
      const stroke = data.stroke;
      applyStrokePoints(stroke.id, stroke.points || [], stroke.color, stroke.size, stroke.tool);
    }
    if (data.type === 'clear') {
      clearWhiteboardLocal();
    }
  });
  whiteboardSocket.addEventListener('close', () => {
    whiteboardReady = false;
    if (whiteboardReconnectHandle) clearTimeout(whiteboardReconnectHandle);
    whiteboardReconnectHandle = setTimeout(connectWhiteboard, 1000);
  });
}

whiteboardCanvas.addEventListener('pointerdown', (event) => {
  event.preventDefault();
  whiteboardCanvas.setPointerCapture(event.pointerId);
  const point = normalizePoint(event);
  activeStrokeId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random());
  activeStroke = {
    id: activeStrokeId,
    color: penColorInput.value,
    size: Number(penSizeInput.value),
    tool: 'pen',
  };
  applyStrokePoints(activeStrokeId, [point], activeStroke.color, activeStroke.size, activeStroke.tool);
  sendWhiteboardEvent({ type: 'stroke-point', clientId: whiteboardClientId, id: activeStrokeId, points: [point], color: activeStroke.color, size: activeStroke.size, tool: activeStroke.tool });
});

whiteboardCanvas.addEventListener('pointermove', (event) => {
  if (!activeStroke) return;
  event.preventDefault();
  const point = normalizePoint(event);
  applyStrokePoints(activeStroke.id, [point], activeStroke.color, activeStroke.size, activeStroke.tool);
  sendWhiteboardEvent({ type: 'stroke-point', clientId: whiteboardClientId, id: activeStroke.id, points: [point], color: activeStroke.color, size: activeStroke.size, tool: activeStroke.tool });
});

function endStroke() {
  if (!activeStroke) return;
  sendWhiteboardEvent({ type: 'stroke-point', clientId: whiteboardClientId, id: activeStroke.id, points: [], color: activeStroke.color, size: activeStroke.size, tool: activeStroke.tool });
  activeStroke = null;
  activeStrokeId = null;
}

whiteboardCanvas.addEventListener('pointerup', endStroke);
whiteboardCanvas.addEventListener('pointercancel', endStroke);
whiteboardCanvas.addEventListener('pointerleave', () => {
  if (activeStroke) endStroke();
});

async function pollTask(taskId, token) {
  if (pollHandle) clearInterval(pollHandle);

  pollHandle = setInterval(async () => {
    try {
      const res = await fetch(`/status/${taskId}`);
      const data = await res.json();
      setStatus(data.status, data.result || data.error || '대기 중');
      cancelBtn.disabled = ['done', 'failed', 'canceled'].includes(data.status);
      if (['done', 'failed'].includes(data.status)) {
        clearInterval(pollHandle);
      }
    } catch (err) {
      clearInterval(pollHandle);
      setStatus('failed', String(err));
    }
  }, 1500);
}

async function submitCommand(command) {
  const token = apiTokenInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }

  setStatus('submitting', '명령을 전송하는 중...');

  const res = await fetch('/command', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Token': token,
    },
    body: JSON.stringify({ command, source: 'web_ui' }),
  });

  const data = await res.json();
  if (!res.ok) {
    setStatus('failed', data.detail || data);
    return;
  }

  taskIdEl.textContent = data.task_id;
  setStatus('pending', '작업이 큐에 등록되었습니다.');
  cancelBtn.disabled = false;
  pollTask(data.task_id, token);
}

async function openBrowserUrl() {
  const token = apiTokenInput.value.trim();
  const url = browserUrlInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!url) {
    alert('URL을 입력하세요.');
    return;
  }
  await submitCommand(url);
}

async function cancelTask() {
  const taskId = taskIdEl.textContent.trim();
  const token = apiTokenInput.value.trim();
  if (!taskId || taskId === '-') {
    return;
  }

  const res = await fetch(`/cancel/${taskId}`, {
    method: 'POST',
    headers: {
      'X-API-Token': token,
    },
  });
  const data = await res.json();
  if (!res.ok) {
    setStatus('failed', data.detail || data);
    return;
  }
  setStatus(data.status, data.cancel_requested ? '취소 요청이 접수되었습니다.' : '작업이 취소되었습니다.');
  cancelBtn.disabled = true;
}

async function dismissReminderOverlay() {
  hideReminderOverlay();
  if (activeReminder) {
    const token = apiTokenInput.value.trim();
    const res = await fetch(`/reminders/${activeReminder.reminder_id}`, {
      method: 'DELETE',
      headers: apiHeaders(token),
    });
    if (res.ok) {
      await loadReminders();
    }
  }
}

sendBtn.addEventListener('click', () => {
  const command = commandInput.value.trim();
  if (!command) return;
  submitCommand(command);
});

openUrlBtn.addEventListener('click', () => {
  openBrowserUrl();
});

cancelBtn.addEventListener('click', cancelTask);
cancelBtn.disabled = true;

mediaUploadBtn.addEventListener('click', uploadSelectedFiles);
favoriteAddBtn.addEventListener('click', addFavoriteVideo);
tvTextSendBtn.addEventListener('click', sendTextToTv);
tvPowerOnBtn.addEventListener('click', powerOnNow);
tvWakeScreenBtn.addEventListener('click', wakeScreenNow);
tvPowerOffBtn.addEventListener('click', powerOffNow);
schedulePowerBtn.addEventListener('click', schedulePowerOff);
reminderAddBtn.addEventListener('click', scheduleReminder);
standbyBtn.addEventListener('click', openStandby);
closeStandbyBtn.addEventListener('click', closeStandby);
newsOverlayBtn.addEventListener('click', openNewsOverlay);
newsOverlayCloseBtn.addEventListener('click', closeNewsOverlay);
reminderOverlayCloseBtn.addEventListener('click', hideReminderOverlay);

clearBoardBtn.addEventListener('click', () => {
  clearWhiteboardLocal();
  sendWhiteboardEvent({ type: 'clear', clientId: whiteboardClientId });
});

commandInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    submitCommand(commandInput.value.trim());
  }
});

for (const chip of document.querySelectorAll('.chip')) {
  chip.addEventListener('click', () => {
    const command = chip.dataset.command;
    commandInput.value = command;
    submitCommand(command);
  });
}

for (const button of document.querySelectorAll('.remote-btn')) {
  button.addEventListener('click', () => {
    const command = button.dataset.command;
    commandInput.value = command;
    submitCommand(command);
  });
}

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeStandby();
    closeNewsOverlay();
  }
});

window.addEventListener('resize', resizeWhiteboardCanvas);
resizeWhiteboardCanvas();
connectWhiteboard();
connectReminders();
void loadWeather();
void loadNews();
void loadMediaLibrary();
void loadPowerSchedules();
void loadReminders();
reminderAtInput.value = formatDateTimeLocalOffset(new Date(Date.now() + 60 * 60 * 1000));
updateStandbyClock();
setInterval(updateStandbyClock, 1000);
setInterval(() => { void loadWeather(); }, 5 * 60 * 1000);
setInterval(() => { void loadNews(); }, 5 * 60 * 1000);
setInterval(() => { void loadPowerSchedules(); }, 30 * 1000);
setInterval(() => { void loadReminders(); }, 30 * 1000);
