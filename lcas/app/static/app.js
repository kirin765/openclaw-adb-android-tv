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
const fridgeNameInput = document.getElementById('fridgeNameInput');
const fridgeCategoryInput = document.getElementById('fridgeCategoryInput');
const fridgeQuantityInput = document.getElementById('fridgeQuantityInput');
const fridgeNoteInput = document.getElementById('fridgeNoteInput');
const fridgeAddBtn = document.getElementById('fridgeAddBtn');
const fridgeRefreshBtn = document.getElementById('fridgeRefreshBtn');
const fridgeStatus = document.getElementById('fridgeStatus');
const fridgeList = document.getElementById('fridgeList');
const recipeList = document.getElementById('recipeList');
const recipeCheckedAt = document.getElementById('recipeCheckedAt');
const calendarTitleInput = document.getElementById('calendarTitleInput');
const calendarLocationInput = document.getElementById('calendarLocationInput');
const calendarStartInput = document.getElementById('calendarStartInput');
const calendarEndInput = document.getElementById('calendarEndInput');
const calendarAttendeesInput = document.getElementById('calendarAttendeesInput');
const calendarTagInput = document.getElementById('calendarTagInput');
const calendarNoteInput = document.getElementById('calendarNoteInput');
const calendarAllDayInput = document.getElementById('calendarAllDayInput');
const calendarAddBtn = document.getElementById('calendarAddBtn');
const calendarRefreshBtn = document.getElementById('calendarRefreshBtn');
const calendarStatus = document.getElementById('calendarStatus');
const calendarTodayList = document.getElementById('calendarTodayList');
const calendarUpcomingList = document.getElementById('calendarUpcomingList');
const calendarCheckedAt = document.getElementById('calendarCheckedAt');
const moodMemberInput = document.getElementById('moodMemberInput');
const moodNoteInput = document.getElementById('moodNoteInput');
const moodSliderInput = document.getElementById('moodSliderInput');
const moodValueLabel = document.getElementById('moodValueLabel');
const moodSaveBtn = document.getElementById('moodSaveBtn');
const moodRefreshBtn = document.getElementById('moodRefreshBtn');
const moodStatus = document.getElementById('moodStatus');
const moodList = document.getElementById('moodList');
const moodCheckedAt = document.getElementById('moodCheckedAt');
const moodChart = document.getElementById('moodChart');
const todoTitleInput = document.getElementById('todoTitleInput');
const todoOwnerInput = document.getElementById('todoOwnerInput');
const todoDueInput = document.getElementById('todoDueInput');
const todoNoteInput = document.getElementById('todoNoteInput');
const todoAddBtn = document.getElementById('todoAddBtn');
const todoRefreshBtn = document.getElementById('todoRefreshBtn');
const todoStatus = document.getElementById('todoStatus');
const todoList = document.getElementById('todoList');
const todoCheckedAt = document.getElementById('todoCheckedAt');
const boardAuthorInput = document.getElementById('boardAuthorInput');
const boardTitleInput = document.getElementById('boardTitleInput');
const boardContentInput = document.getElementById('boardContentInput');
const boardPinnedInput = document.getElementById('boardPinnedInput');
const boardAddBtn = document.getElementById('boardAddBtn');
const boardRefreshBtn = document.getElementById('boardRefreshBtn');
const boardStatus = document.getElementById('boardStatus');
const boardList = document.getElementById('boardList');
const boardCheckedAt = document.getElementById('boardCheckedAt');
const tvTextInput = document.getElementById('tvTextInput');
const tvTextSendBtn = document.getElementById('tvTextSendBtn');
const tvPowerOnBtn = document.getElementById('tvPowerOnBtn');
const tvWakeScreenBtn = document.getElementById('tvWakeScreenBtn');
const tvPowerOffBtn = document.getElementById('tvPowerOffBtn');
const powerDelayInput = document.getElementById('powerDelayInput');
const schedulePowerBtn = document.getElementById('schedulePowerBtn');
const powerStatus = document.getElementById('powerStatus');
const powerScheduleList = document.getElementById('powerScheduleList');
const tvAppsSearchInput = document.getElementById('tvAppsSearchInput');
const tvAppsRefreshBtn = document.getElementById('tvAppsRefreshBtn');
const tvAppsStatus = document.getElementById('tvAppsStatus');
const tvAppsList = document.getElementById('tvAppsList');
const tvAppsCheckedAt = document.getElementById('tvAppsCheckedAt');
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
const mirrorLabelInput = document.getElementById('mirrorLabelInput');
const mirrorStartBtn = document.getElementById('mirrorStartBtn');
const mirrorStopBtn = document.getElementById('mirrorStopBtn');
const mirrorStatus = document.getElementById('mirrorStatus');
const mirrorImage = document.getElementById('mirrorImage');
const mirrorEmpty = document.getElementById('mirrorEmpty');
const mirrorOverlayBtn = document.getElementById('mirrorOverlayBtn');
const mirrorOverlay = document.getElementById('mirrorOverlay');
const mirrorOverlayImage = document.getElementById('mirrorOverlayImage');
const mirrorOverlayTitle = document.getElementById('mirrorOverlayTitle');
const mirrorOverlayMeta = document.getElementById('mirrorOverlayMeta');
const mirrorOverlayCloseBtn = document.getElementById('mirrorOverlayCloseBtn');
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
const moodChartCtx = moodChart.getContext('2d');
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
let fridgeState = { items: [], recommendations: [], checked_at: null };
let calendarState = { events: [], today_events: [], upcoming_events: [], checked_at: null };
let moodState = { records: [], series: [], members: [], checked_at: null };
let todoState = { items: [], checked_at: null };
let boardState = { posts: [], checked_at: null };
let tvAppsState = { apps: [], checked_at: null, error: null };
let reminderState = [];
let newsState = null;
let mirrorState = null;
let currentPreviewType = 'none';
let reminderSocket = null;
let reminderReconnectHandle = null;
let activeReminder = null;
let boardSocket = null;
let boardReconnectHandle = null;
let moodSocket = null;
let moodReconnectHandle = null;
let todoSocket = null;
let todoReconnectHandle = null;
let mirrorSocket = null;
let mirrorReconnectHandle = null;
let mirrorCaptureStream = null;
let mirrorCaptureVideo = null;
let mirrorCaptureCanvas = null;
let mirrorCaptureCtx = null;
let mirrorCaptureTimer = null;
let mirrorCaptureFrameId = null;
let mirrorOverlayActive = false;

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

function fridgeCategoryLabel(category) {
  if (category === 'side_dish') return '반찬';
  return '재료';
}

function renderFridgeItems(items) {
  fridgeList.innerHTML = '';
  if (!items.length) {
    fridgeList.innerHTML = '<div class="fineprint">등록된 재료나 반찬이 없습니다.</div>';
    return;
  }

  for (const item of items) {
    const card = document.createElement('div');
    card.className = 'fridge-item';
    card.innerHTML = `
      <strong>${item.name}</strong>
      <div class="meta">${fridgeCategoryLabel(item.category)}${item.quantity ? ` · ${item.quantity}` : ''}</div>
      <div class="meta">${item.note || '메모 없음'}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/fridge/items/${item.fridge_item_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        fridgeStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      fridgeStatus.textContent = '항목을 삭제했습니다.';
      await loadFridgeState();
    });
    actions.append(deleteBtn);
    card.append(actions);
    fridgeList.appendChild(card);
  }
}

function renderRecipeList(recommendations, checkedAt) {
  recipeList.innerHTML = '';
  if (!recommendations.length) {
    recipeList.innerHTML = '<div class="fineprint">등록된 재료를 바탕으로 추천할 레시피가 없습니다.</div>';
    recipeCheckedAt.textContent = checkedAt || '';
    return;
  }

  for (const recipe of recommendations) {
    const card = document.createElement('div');
    card.className = 'recipe-item';
    card.innerHTML = `
      <strong>${recipe.title}</strong>
      <div class="meta">점수 ${recipe.score} · ${recipe.description}</div>
      <div class="recipe-tags">
        <span>맞는 재료: ${recipe.matched_items.length ? recipe.matched_items.join(', ') : '없음'}</span>
        <span>부족한 재료: ${recipe.missing_items.length ? recipe.missing_items.join(', ') : '없음'}</span>
      </div>
    `;
    if (recipe.steps && recipe.steps.length) {
      const steps = document.createElement('ol');
      steps.className = 'recipe-steps';
      for (const step of recipe.steps) {
        const li = document.createElement('li');
        li.textContent = step;
        steps.appendChild(li);
      }
      card.appendChild(steps);
    }
    recipeList.appendChild(card);
  }

  recipeCheckedAt.textContent = checkedAt || '';
}

function formatCalendarTime(value) {
  if (!value) return '시간 정보 없음';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString('ko-KR', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function renderCalendarItems(items, mount, emptyMessage) {
  mount.innerHTML = '';
  if (!items.length) {
    mount.innerHTML = `<div class="fineprint">${emptyMessage}</div>`;
    return;
  }

  for (const event of items) {
    const card = document.createElement('div');
    card.className = 'calendar-item';
    card.innerHTML = `
      <strong>${event.title}</strong>
      <div class="meta">${event.all_day ? '하루 일정' : `${formatCalendarTime(event.start_at)}${event.end_at ? ` ~ ${formatCalendarTime(event.end_at)}` : ''}`}</div>
      <div class="calendar-tags">${event.tag ? `<span class="calendar-tag calendar-tag-brown">${event.tag}</span>` : ''}</div>
      <div class="meta">${event.location || '장소 없음'}</div>
      <div class="meta">${event.attendees && event.attendees.length ? event.attendees.join(', ') : '가족 구성원 미지정'}</div>
      <div class="meta">${event.note || '메모 없음'}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/family-calendar/events/${event.calendar_event_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        calendarStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      calendarStatus.textContent = '일정을 삭제했습니다.';
      await loadCalendarState();
    });
    actions.append(deleteBtn);
    card.append(actions);
    mount.appendChild(card);
  }
}

function moodLabelForValue(value) {
  const labels = {
    1: '매우 힘듦',
    2: '조금 힘듦',
    3: '보통',
    4: '좋음',
    5: '매우 좋음',
  };
  return labels[value] || '보통';
}

function updateMoodValueLabel() {
  const value = Number(moodSliderInput.value);
  moodValueLabel.textContent = moodLabelForValue(value);
}

function renderMoodRecords(records) {
  moodList.innerHTML = '';
  if (!records.length) {
    moodList.innerHTML = '<div class="fineprint">아직 감정 기록이 없습니다.</div>';
    return;
  }

  for (const record of records) {
    const card = document.createElement('div');
    card.className = 'mood-item';
    card.innerHTML = `
      <div class="mood-row">
        <strong>${record.member}</strong>
        <span class="mood-badge mood-badge-${record.mood}">${moodLabelForValue(record.mood)}</span>
      </div>
      <div class="meta">${formatCalendarTime(record.created_at)}</div>
      <div class="meta">${record.note || '메모 없음'}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/family-mood/records/${record.mood_record_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        moodStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      moodStatus.textContent = '감정 기록을 삭제했습니다.';
      await loadMoodState();
    });
    actions.append(deleteBtn);
    card.append(actions);
    moodList.appendChild(card);
  }
}

function resizeMoodChartCanvas() {
  const rect = moodChart.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  moodChart.width = Math.max(1, Math.floor(rect.width * dpr));
  moodChart.height = Math.max(1, Math.floor(rect.height * dpr));
  moodChartCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  drawMoodChart();
}

function drawMoodChart() {
  const width = moodChart.getBoundingClientRect().width;
  const height = moodChart.getBoundingClientRect().height;
  moodChartCtx.clearRect(0, 0, width, height);

  const series = moodState.series || [];
  if (!series.length || series.every((item) => !item.points || !item.points.length)) {
    moodChartCtx.fillStyle = '#94a3b8';
    moodChartCtx.font = '14px system-ui, sans-serif';
    moodChartCtx.fillText('기록이 쌓이면 멤버별 감정 추이가 여기에 표시됩니다.', 16, 24);
    return;
  }

  const padding = { top: 24, right: 16, bottom: 36, left: 48 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const today = new Date();
  const dates = [];
  for (let offset = 13; offset >= 0; offset -= 1) {
    const day = new Date(today);
    day.setDate(today.getDate() - offset);
    dates.push(day.toISOString().slice(0, 10));
  }

  moodChartCtx.strokeStyle = 'rgba(148, 163, 184, 0.24)';
  moodChartCtx.fillStyle = '#cbd5e1';
  moodChartCtx.lineWidth = 1;
  moodChartCtx.font = '12px system-ui, sans-serif';

  for (let level = 1; level <= 5; level += 1) {
    const y = padding.top + chartHeight - ((level - 1) / 4) * chartHeight;
    moodChartCtx.beginPath();
    moodChartCtx.moveTo(padding.left, y);
    moodChartCtx.lineTo(width - padding.right, y);
    moodChartCtx.stroke();
    moodChartCtx.fillText(String(level), 12, y + 4);
  }

  for (let i = 0; i < dates.length; i += 1) {
    if (i % 2 !== 0) continue;
    const x = padding.left + (i / (dates.length - 1)) * chartWidth;
    moodChartCtx.beginPath();
    moodChartCtx.moveTo(x, padding.top);
    moodChartCtx.lineTo(x, padding.top + chartHeight);
    moodChartCtx.stroke();
    moodChartCtx.save();
    moodChartCtx.translate(x - 12, height - 12);
    moodChartCtx.rotate(-Math.PI / 4);
    moodChartCtx.fillText(dates[i].slice(5), 0, 0);
    moodChartCtx.restore();
  }

  moodChartCtx.font = '12px system-ui, sans-serif';
  let legendY = 16;
  for (const item of series.slice(0, 4)) {
    moodChartCtx.fillStyle = item.color || '#60a5fa';
    moodChartCtx.fillRect(width - 150, legendY - 8, 10, 10);
    moodChartCtx.fillStyle = '#e2e8f0';
    moodChartCtx.fillText(item.member, width - 132, legendY);
    legendY += 16;
  }

  for (const item of series) {
    const pointByDate = new Map((item.points || []).map((point) => [point.date, point]));
    moodChartCtx.strokeStyle = item.color || '#60a5fa';
    moodChartCtx.lineWidth = 2;
    moodChartCtx.beginPath();
    let segmentStarted = false;

    for (let index = 0; index < dates.length; index += 1) {
      const dateKey = dates[index];
      const point = pointByDate.get(dateKey);
      if (!point) {
        segmentStarted = false;
        continue;
      }
      const x = padding.left + (index / (dates.length - 1)) * chartWidth;
      const y = padding.top + chartHeight - ((point.mood - 1) / 4) * chartHeight;
      if (!segmentStarted) {
        moodChartCtx.moveTo(x, y);
        segmentStarted = true;
      } else {
        moodChartCtx.lineTo(x, y);
      }
    }
    moodChartCtx.stroke();

    for (let index = 0; index < dates.length; index += 1) {
      const dateKey = dates[index];
      const point = pointByDate.get(dateKey);
      if (!point) continue;
      const x = padding.left + (index / (dates.length - 1)) * chartWidth;
      const y = padding.top + chartHeight - ((point.mood - 1) / 4) * chartHeight;
      moodChartCtx.beginPath();
      moodChartCtx.fillStyle = item.color || '#60a5fa';
      moodChartCtx.arc(x, y, 3.5, 0, Math.PI * 2);
      moodChartCtx.fill();
    }
  }
}

function formatTodoCheckedAt(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return `마지막 확인 ${value}`;
  return `마지막 확인 ${date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })}`;
}

function renderTodoItems(items) {
  todoList.innerHTML = '';
  if (!items.length) {
    todoList.innerHTML = '<div class="fineprint">등록된 TODO가 없습니다.</div>';
    return;
  }

  for (const item of items) {
    const card = document.createElement('div');
    card.className = item.done ? 'todo-item done' : 'todo-item';
    card.innerHTML = `
      <div class="todo-row">
        <strong>${item.title}</strong>
        <span class="todo-badge ${item.done ? 'todo-badge-done' : 'todo-badge-open'}">${item.done ? '완료' : '진행중'}</span>
      </div>
      <div class="meta">${item.owner || '담당자 없음'}${item.due_at ? ` · ${formatCalendarTime(item.due_at)}` : ''}</div>
      <div class="meta">${item.note || '메모 없음'}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';

    const toggleLabel = document.createElement('label');
    toggleLabel.className = 'inline-check';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = Boolean(item.done);
    checkbox.addEventListener('change', async () => {
      const res = await fetch(`/family-todo/items/${item.todo_item_id}`, {
        method: 'PATCH',
        headers: apiHeaders(apiTokenInput.value.trim(), { 'Content-Type': 'application/json' }),
        body: JSON.stringify({ done: checkbox.checked }),
      });
      const data = await res.json();
      if (!res.ok) {
        todoStatus.textContent = data.detail || '상태 변경 실패';
        checkbox.checked = !checkbox.checked;
        return;
      }
      todoStatus.textContent = checkbox.checked ? 'TODO를 완료로 표시했습니다.' : 'TODO를 미완료로 되돌렸습니다.';
      await loadTodoState();
    });
    const checkboxText = document.createElement('span');
    checkboxText.textContent = '완료';
    toggleLabel.append(checkbox, checkboxText);

    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/family-todo/items/${item.todo_item_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        todoStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      todoStatus.textContent = 'TODO를 삭제했습니다.';
      await loadTodoState();
    });

    actions.append(toggleLabel, deleteBtn);
    card.append(actions);
    todoList.appendChild(card);
  }
}

async function loadTodoState() {
  try {
    const res = await fetch('/family-todo/state');
    const data = await res.json();
    if (!res.ok) {
      todoStatus.textContent = data.detail || 'TODO 목록을 불러오지 못했습니다.';
      return;
    }
    todoState = data;
    renderTodoItems(data.items || []);
    todoCheckedAt.textContent = formatTodoCheckedAt(data.checked_at);
  } catch (err) {
    todoStatus.textContent = `TODO 목록 오류: ${err}`;
  }
}

function connectTodo() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  todoSocket = new WebSocket(`${protocol}//${window.location.host}/ws/family-todo`);
  todoSocket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'snapshot') {
      todoState = {
        items: data.items || [],
        checked_at: data.checked_at || new Date().toISOString(),
      };
      renderTodoItems(todoState.items);
      todoCheckedAt.textContent = formatTodoCheckedAt(todoState.checked_at);
    }
  });
  todoSocket.addEventListener('close', () => {
    if (todoReconnectHandle) clearTimeout(todoReconnectHandle);
    todoReconnectHandle = setTimeout(connectTodo, 1000);
  });
}

function formatBoardCheckedAt(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return `마지막 확인 ${value}`;
  return `마지막 확인 ${date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })}`;
}

function renderBoardPosts(posts) {
  boardList.innerHTML = '';
  if (!posts.length) {
    boardList.innerHTML = '<div class="fineprint">등록된 게시글이 없습니다.</div>';
    return;
  }

  for (const post of posts) {
    const card = document.createElement('div');
    card.className = post.pinned ? 'board-item pinned' : 'board-item';
    card.innerHTML = `
      <div class="board-head">
        <strong>${post.title}</strong>
        ${post.pinned ? '<span class="board-badge">고정</span>' : ''}
      </div>
      <div class="meta">${post.author} · ${formatCalendarTime(post.created_at)}</div>
      <div class="board-content">${post.content}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.textContent = '삭제';
    deleteBtn.addEventListener('click', async () => {
      const res = await fetch(`/family-board/posts/${post.board_post_id}`, {
        method: 'DELETE',
        headers: apiHeaders(apiTokenInput.value.trim()),
      });
      const data = await res.json();
      if (!res.ok) {
        boardStatus.textContent = data.detail || '삭제 실패';
        return;
      }
      boardStatus.textContent = '게시글을 삭제했습니다.';
      await loadBoardState();
    });
    actions.append(deleteBtn);
    card.append(actions);
    boardList.appendChild(card);
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

function formatTvAppsCheckedAt(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return `마지막 확인 ${value}`;
  return `마지막 확인 ${date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })}`;
}

function filteredTvApps() {
  const query = tvAppsSearchInput.value.trim().toLowerCase();
  const apps = tvAppsState.apps || [];
  if (!query) {
    return apps;
  }
  return apps.filter((app) => {
    const label = (app.label || '').toLowerCase();
    const packageName = (app.package_name || '').toLowerCase();
    const activity = (app.activity_name || '').toLowerCase();
    return label.includes(query) || packageName.includes(query) || activity.includes(query);
  });
}

function renderTvApps() {
  const apps = filteredTvApps();
  tvAppsList.innerHTML = '';
  if (!apps.length) {
    const message = tvAppsState.error ? `앱 목록을 불러오지 못했습니다: ${tvAppsState.error}` : '표시할 앱이 없습니다.';
    tvAppsList.innerHTML = `<div class="fineprint">${message}</div>`;
    tvAppsStatus.textContent = tvAppsState.error || '앱 목록을 불러왔습니다.';
    tvAppsCheckedAt.textContent = formatTvAppsCheckedAt(tvAppsState.checked_at);
    return;
  }

  tvAppsStatus.textContent = tvAppsState.error || `${apps.length}개의 앱을 찾았습니다.`;
  tvAppsCheckedAt.textContent = formatTvAppsCheckedAt(tvAppsState.checked_at);

  for (const app of apps) {
    const card = document.createElement('div');
    card.className = 'tv-app-item';
    card.innerHTML = `
      <strong>${app.label || app.package_name}</strong>
      <div class="meta">${app.package_name}</div>
      <div class="meta">${app.activity_name || '메인 런처'}</div>
    `;
    const actions = document.createElement('div');
    actions.className = 'actions';
    const launchBtn = document.createElement('button');
    launchBtn.type = 'button';
    launchBtn.textContent = '실행';
    launchBtn.addEventListener('click', () => {
      void launchTvApp(app);
    });
    actions.append(launchBtn);
    card.append(actions);
    tvAppsList.appendChild(card);
  }
}

async function loadTvApps() {
  try {
    const res = await fetch('/tv/apps');
    const data = await res.json();
    if (!res.ok) {
      tvAppsState = { apps: [], checked_at: new Date().toISOString(), error: data.detail || '앱 목록을 불러오지 못했습니다.' };
      renderTvApps();
      return;
    }
    tvAppsState = data;
    renderTvApps();
  } catch (err) {
    tvAppsState = { apps: [], checked_at: new Date().toISOString(), error: String(err) };
    renderTvApps();
  }
}

async function launchTvApp(app) {
  const token = apiTokenInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  const res = await fetch('/tv/apps/launch', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({
      package_name: app.package_name,
      activity_name: app.activity_name || '',
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    tvAppsStatus.textContent = data.detail || '앱 실행 실패';
    return;
  }
  tvAppsStatus.textContent = `${app.label || app.package_name}을(를) 실행했습니다.`;
  taskIdEl.textContent = '-';
  setStatus('done', data.message || '앱 실행 완료');
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

function renderMirrorState(state) {
  mirrorState = state;
  const hasFrame = Boolean(state && state.frame_data_url);
  if (hasFrame) {
    mirrorImage.src = state.frame_data_url;
    mirrorOverlayImage.src = state.frame_data_url;
    mirrorEmpty.style.display = 'none';
  } else {
    mirrorImage.removeAttribute('src');
    mirrorOverlayImage.removeAttribute('src');
    mirrorEmpty.style.display = 'grid';
  }
  mirrorStatus.textContent = state && state.active
    ? `공유 중: ${state.source_label || '미지정'} · 프레임 ${state.frame_count || 0}`
    : '지원되는 모바일 브라우저에서 시작할 수 있습니다.';
  mirrorOverlayTitle.textContent = state && state.active ? (state.source_label || '실시간 미러링') : '대기 중';
  mirrorOverlayMeta.textContent = state && state.active
    ? `업데이트 ${state.updated_at || '-'} · 프레임 ${state.frame_count || 0}`
    : '아직 공유 중인 화면이 없습니다.';
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

function formatRecipeCheckedAt(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return `마지막 확인 ${value}`;
  return `마지막 확인 ${date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })}`;
}

async function loadFridgeState() {
  try {
    const res = await fetch('/fridge/state');
    const data = await res.json();
    if (!res.ok) {
      fridgeStatus.textContent = data.detail || '냉장고 상태를 불러오지 못했습니다.';
      return;
    }
    fridgeState = data;
    renderFridgeItems(data.items || []);
    renderRecipeList(data.recommendations || [], formatRecipeCheckedAt(data.checked_at));
  } catch (err) {
    fridgeStatus.textContent = `냉장고 상태 오류: ${err}`;
  }
}

function formatCalendarCheckedAt(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return `마지막 확인 ${value}`;
  return `마지막 확인 ${date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })}`;
}

async function loadCalendarState() {
  try {
    const res = await fetch('/family-calendar/state');
    const data = await res.json();
    if (!res.ok) {
      calendarStatus.textContent = data.detail || '가족 캘린더를 불러오지 못했습니다.';
      return;
    }
    calendarState = data;
    renderCalendarItems(data.today_events || [], calendarTodayList, '오늘 일정이 없습니다.');
    renderCalendarItems(data.upcoming_events || [], calendarUpcomingList, '다가오는 일정이 없습니다.');
    calendarCheckedAt.textContent = formatCalendarCheckedAt(data.checked_at);
  } catch (err) {
    calendarStatus.textContent = `가족 캘린더 오류: ${err}`;
  }
}

async function loadMoodState() {
  try {
    const res = await fetch('/family-mood/state');
    const data = await res.json();
    if (!res.ok) {
      moodStatus.textContent = data.detail || '감정 기록을 불러오지 못했습니다.';
      return;
    }
    moodState = data;
    renderMoodRecords(data.records || []);
    moodCheckedAt.textContent = formatCalendarCheckedAt(data.checked_at);
    drawMoodChart();
  } catch (err) {
    moodStatus.textContent = `감정 기록 오류: ${err}`;
  }
}

function connectMood() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  moodSocket = new WebSocket(`${protocol}//${window.location.host}/ws/family-mood`);
  moodSocket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'snapshot') {
      moodState = {
        records: data.records || [],
        series: moodState.series || [],
        members: moodState.members || [],
        checked_at: data.checked_at || new Date().toISOString(),
      };
      void loadMoodState();
    }
  });
  moodSocket.addEventListener('close', () => {
    if (moodReconnectHandle) clearTimeout(moodReconnectHandle);
    moodReconnectHandle = setTimeout(connectMood, 1000);
  });
}

async function loadBoardState() {
  try {
    const res = await fetch('/family-board/state');
    const data = await res.json();
    if (!res.ok) {
      boardStatus.textContent = data.detail || '가족 게시판을 불러오지 못했습니다.';
      return;
    }
    boardState = data;
    renderBoardPosts(data.posts || []);
    boardCheckedAt.textContent = formatBoardCheckedAt(data.checked_at);
  } catch (err) {
    boardStatus.textContent = `가족 게시판 오류: ${err}`;
  }
}

function connectBoard() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  boardSocket = new WebSocket(`${protocol}//${window.location.host}/ws/family-board`);
  boardSocket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'snapshot') {
      boardState = { posts: data.posts || [], checked_at: data.checked_at || new Date().toISOString() };
      renderBoardPosts(boardState.posts);
      boardCheckedAt.textContent = formatBoardCheckedAt(boardState.checked_at);
    }
  });
  boardSocket.addEventListener('close', () => {
    if (boardReconnectHandle) clearTimeout(boardReconnectHandle);
    boardReconnectHandle = setTimeout(connectBoard, 1000);
  });
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

async function loadMirrorState() {
  try {
    const res = await fetch('/mirror/state');
    const data = await res.json();
    if (!res.ok) {
      mirrorStatus.textContent = data.detail || '미러링 상태를 불러오지 못했습니다.';
      return;
    }
    renderMirrorState(data);
  } catch (err) {
    mirrorStatus.textContent = `미러링 상태 오류: ${err}`;
  }
}

function connectMirror() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  mirrorSocket = new WebSocket(`${protocol}//${window.location.host}/ws/mirror`);
  mirrorSocket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'snapshot' || data.type === 'frame' || data.type === 'stop') {
      renderMirrorState(data.mirror || {});
    }
  });
  mirrorSocket.addEventListener('close', () => {
    if (mirrorReconnectHandle) clearTimeout(mirrorReconnectHandle);
    mirrorReconnectHandle = setTimeout(connectMirror, 1000);
  });
}

function stopMirrorCapture() {
  if (mirrorCaptureTimer) {
    clearTimeout(mirrorCaptureTimer);
    mirrorCaptureTimer = null;
  }
  if (mirrorCaptureFrameId) {
    cancelAnimationFrame(mirrorCaptureFrameId);
    mirrorCaptureFrameId = null;
  }
  if (mirrorCaptureVideo) {
    mirrorCaptureVideo.pause();
    mirrorCaptureVideo.srcObject = null;
    mirrorCaptureVideo = null;
  }
  if (mirrorCaptureStream) {
    for (const track of mirrorCaptureStream.getTracks()) {
      track.stop();
    }
    mirrorCaptureStream = null;
  }
  if (mirrorSocket && mirrorSocket.readyState === WebSocket.OPEN) {
    mirrorSocket.send(JSON.stringify({ type: 'stop' }));
  }
  renderMirrorState({
    active: false,
    source_label: mirrorState && mirrorState.source_label ? mirrorState.source_label : '',
    frame_data_url: null,
    started_at: mirrorState && mirrorState.started_at ? mirrorState.started_at : null,
    updated_at: mirrorState && mirrorState.updated_at ? mirrorState.updated_at : null,
    frame_count: mirrorState && mirrorState.frame_count ? mirrorState.frame_count : 0,
  });
  mirrorStatus.textContent = '미러링이 중지되었습니다.';
}

function sendMirrorFrame() {
  if (!mirrorCaptureStream || !mirrorCaptureVideo || !mirrorCaptureCanvas || !mirrorCaptureCtx) {
    return;
  }
  if (mirrorCaptureVideo.readyState < 2 || !mirrorCaptureVideo.videoWidth || !mirrorCaptureVideo.videoHeight) {
    mirrorCaptureTimer = setTimeout(sendMirrorFrame, 120);
    return;
  }
  const maxWidth = 960;
  const width = mirrorCaptureVideo.videoWidth;
  const height = mirrorCaptureVideo.videoHeight;
  const scale = Math.min(1, maxWidth / width);
  const canvasWidth = Math.max(1, Math.round(width * scale));
  const canvasHeight = Math.max(1, Math.round(height * scale));
  mirrorCaptureCanvas.width = canvasWidth;
  mirrorCaptureCanvas.height = canvasHeight;
  mirrorCaptureCtx.drawImage(mirrorCaptureVideo, 0, 0, canvasWidth, canvasHeight);
  const frameDataUrl = mirrorCaptureCanvas.toDataURL('image/jpeg', 0.72);
  if (mirrorSocket && mirrorSocket.readyState === WebSocket.OPEN) {
    mirrorSocket.send(JSON.stringify({
      type: 'frame',
      frame_data_url: frameDataUrl,
      source_label: mirrorLabelInput.value.trim(),
      started_at: new Date().toISOString(),
    }));
  }
  mirrorCaptureTimer = setTimeout(sendMirrorFrame, 160);
}

async function startMirrorCapture() {
  const sourceLabel = mirrorLabelInput.value.trim() || 'Mobile';
  if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
    mirrorStatus.textContent = '이 브라우저는 화면 공유를 지원하지 않습니다.';
    return;
  }
  try {
    stopMirrorCapture();
    mirrorStatus.textContent = '화면 공유 권한을 요청하는 중...';
    const stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: false });
    mirrorCaptureStream = stream;
    mirrorCaptureVideo = document.createElement('video');
    mirrorCaptureVideo.autoplay = true;
    mirrorCaptureVideo.muted = true;
    mirrorCaptureVideo.playsInline = true;
    mirrorCaptureVideo.srcObject = stream;
    await mirrorCaptureVideo.play();
    mirrorCaptureCanvas = document.createElement('canvas');
    mirrorCaptureCtx = mirrorCaptureCanvas.getContext('2d', { alpha: false });
    if (mirrorSocket && mirrorSocket.readyState === WebSocket.OPEN) {
      mirrorSocket.send(JSON.stringify({
        type: 'start',
        source_label: sourceLabel,
        started_at: new Date().toISOString(),
      }));
    }
    mirrorStatus.textContent = '미러링을 전송하는 중입니다.';
    sendMirrorFrame();
    stream.getVideoTracks()[0].addEventListener('ended', () => {
      stopMirrorCapture();
      mirrorStatus.textContent = '미러링이 중지되었습니다.';
    });
  } catch (err) {
    mirrorStatus.textContent = `미러링 시작 실패: ${err}`;
    stopMirrorCapture();
  }
}

function openMirrorOverlay() {
  mirrorOverlay.classList.remove('hidden');
  mirrorOverlayActive = true;
  if (mirrorState) {
    renderMirrorState(mirrorState);
  }
}

function closeMirrorOverlay() {
  mirrorOverlay.classList.add('hidden');
  mirrorOverlayActive = false;
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

async function addFridgeItem() {
  const token = apiTokenInput.value.trim();
  const name = fridgeNameInput.value.trim();
  const category = fridgeCategoryInput.value;
  const quantity = fridgeQuantityInput.value.trim();
  const note = fridgeNoteInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!name) {
    fridgeStatus.textContent = '이름을 입력하세요.';
    return;
  }
  const res = await fetch('/fridge/items', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ name, category, quantity, note }),
  });
  const data = await res.json();
  if (!res.ok) {
    fridgeStatus.textContent = data.detail || '냉장고 항목 등록 실패';
    return;
  }
  fridgeStatus.textContent = `${data.name}을(를) 등록했습니다.`;
  fridgeNameInput.value = '';
  fridgeQuantityInput.value = '';
  fridgeNoteInput.value = '';
  fridgeNameInput.focus();
  await loadFridgeState();
}

async function addCalendarEvent() {
  const token = apiTokenInput.value.trim();
  const title = calendarTitleInput.value.trim();
  const startAt = calendarStartInput.value.trim();
  const endAt = calendarEndInput.value.trim();
  const location = calendarLocationInput.value.trim();
  const attendees = calendarAttendeesInput.value.trim();
  const tag = calendarTagInput.value.trim();
  const note = calendarNoteInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!title || !startAt) {
    calendarStatus.textContent = '제목과 시작 시간은 필수입니다.';
    return;
  }
  if (endAt && endAt <= startAt) {
    calendarStatus.textContent = '종료 시간은 시작 시간보다 뒤여야 합니다.';
    return;
  }
  const res = await fetch('/family-calendar/events', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({
      title,
      start_at: startAt,
      end_at: endAt,
      location,
      attendees,
      tag,
      note,
      all_day: calendarAllDayInput.checked,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    calendarStatus.textContent = data.detail || '가족 캘린더 등록 실패';
    return;
  }
  calendarStatus.textContent = `${data.title} 일정을 등록했습니다.`;
  calendarTitleInput.value = '';
  calendarLocationInput.value = '';
  calendarStartInput.value = '';
  calendarEndInput.value = '';
  calendarAttendeesInput.value = '';
  calendarTagInput.value = '김은영똥';
  calendarNoteInput.value = '';
  calendarAllDayInput.checked = false;
  await loadCalendarState();
}

async function addMoodRecord() {
  const token = apiTokenInput.value.trim();
  const member = moodMemberInput.value.trim();
  const note = moodNoteInput.value.trim();
  const mood = Number(moodSliderInput.value);
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!member) {
    moodStatus.textContent = '가족 구성원 이름을 입력하세요.';
    return;
  }
  const res = await fetch('/family-mood/records', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ member, mood, note }),
  });
  const data = await res.json();
  if (!res.ok) {
    moodStatus.textContent = data.detail || '감정 기록 실패';
    return;
  }
  moodStatus.textContent = `${data.member}의 감정을 저장했습니다.`;
  moodNoteInput.value = '';
  await loadMoodState();
}

async function addTodoItem() {
  const token = apiTokenInput.value.trim();
  const title = todoTitleInput.value.trim();
  const owner = todoOwnerInput.value.trim();
  const dueAt = todoDueInput.value.trim();
  const note = todoNoteInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!title) {
    todoStatus.textContent = '할 일을 입력하세요.';
    return;
  }
  const res = await fetch('/family-todo/items', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({ title, owner, due_at: dueAt, note }),
  });
  const data = await res.json();
  if (!res.ok) {
    todoStatus.textContent = data.detail || 'TODO 등록 실패';
    return;
  }
  todoStatus.textContent = 'TODO를 등록했습니다.';
  todoTitleInput.value = '';
  todoOwnerInput.value = '';
  todoDueInput.value = '';
  todoNoteInput.value = '';
  todoTitleInput.focus();
  await loadTodoState();
}

async function addBoardPost() {
  const token = apiTokenInput.value.trim();
  const author = boardAuthorInput.value.trim();
  const title = boardTitleInput.value.trim();
  const content = boardContentInput.value.trim();
  if (!token) {
    alert('API 토큰을 입력하세요.');
    return;
  }
  if (!author || !title || !content) {
    boardStatus.textContent = '작성자, 제목, 내용은 필수입니다.';
    return;
  }
  const res = await fetch('/family-board/posts', {
    method: 'POST',
    headers: apiHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify({
      author,
      title,
      content,
      pinned: boardPinnedInput.checked,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    boardStatus.textContent = data.detail || '게시글 등록 실패';
    return;
  }
  boardStatus.textContent = '게시글을 등록했습니다.';
  boardTitleInput.value = '';
  boardContentInput.value = '';
  boardPinnedInput.checked = false;
  await loadBoardState();
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
fridgeAddBtn.addEventListener('click', addFridgeItem);
fridgeRefreshBtn.addEventListener('click', () => {
  void loadFridgeState();
});
calendarAddBtn.addEventListener('click', addCalendarEvent);
calendarRefreshBtn.addEventListener('click', () => {
  void loadCalendarState();
});
updateMoodValueLabel();
moodSliderInput.addEventListener('input', updateMoodValueLabel);
moodSaveBtn.addEventListener('click', addMoodRecord);
moodRefreshBtn.addEventListener('click', () => {
  void loadMoodState();
});
todoAddBtn.addEventListener('click', addTodoItem);
todoRefreshBtn.addEventListener('click', () => {
  void loadTodoState();
});
boardAddBtn.addEventListener('click', addBoardPost);
boardRefreshBtn.addEventListener('click', () => {
  void loadBoardState();
});
tvAppsRefreshBtn.addEventListener('click', () => {
  void loadTvApps();
});
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
mirrorStartBtn.addEventListener('click', startMirrorCapture);
mirrorStopBtn.addEventListener('click', stopMirrorCapture);
mirrorOverlayBtn.addEventListener('click', openMirrorOverlay);
mirrorOverlayCloseBtn.addEventListener('click', closeMirrorOverlay);
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

for (const element of [fridgeNameInput, fridgeQuantityInput, fridgeNoteInput]) {
  element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      addFridgeItem();
    }
  });
}

for (const element of [calendarTitleInput, calendarLocationInput, calendarStartInput, calendarEndInput, calendarAttendeesInput, calendarNoteInput]) {
  element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      addCalendarEvent();
    }
  });
}

for (const element of [moodMemberInput, moodNoteInput]) {
  element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      addMoodRecord();
    }
  });
}

for (const element of [todoTitleInput, todoOwnerInput, todoDueInput, todoNoteInput]) {
  element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      addTodoItem();
    }
  });
}

for (const element of [boardAuthorInput, boardTitleInput, boardContentInput]) {
  element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      addBoardPost();
    }
  });
}

tvAppsSearchInput.addEventListener('input', () => {
  renderTvApps();
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
    closeMirrorOverlay();
  }
});

window.addEventListener('beforeunload', () => {
  stopMirrorCapture();
  if (moodSocket && moodSocket.readyState === WebSocket.OPEN) {
    moodSocket.close();
  }
  if (todoSocket && todoSocket.readyState === WebSocket.OPEN) {
    todoSocket.close();
  }
});

window.addEventListener('resize', resizeWhiteboardCanvas);
window.addEventListener('resize', resizeMoodChartCanvas);
resizeWhiteboardCanvas();
resizeMoodChartCanvas();
connectWhiteboard();
connectReminders();
connectMood();
connectTodo();
connectBoard();
connectMirror();
void loadWeather();
void loadNews();
void loadMediaLibrary();
void loadFridgeState();
void loadCalendarState();
void loadMoodState();
void loadTodoState();
void loadBoardState();
void loadTvApps();
void loadPowerSchedules();
void loadReminders();
void loadMirrorState();
reminderAtInput.value = formatDateTimeLocalOffset(new Date(Date.now() + 60 * 60 * 1000));
calendarStartInput.value = formatDateTimeLocalOffset(new Date(Date.now() + 24 * 60 * 60 * 1000));
calendarEndInput.value = formatDateTimeLocalOffset(new Date(Date.now() + 25 * 60 * 60 * 1000));
calendarTagInput.value = '김은영똥';
updateStandbyClock();
setInterval(updateStandbyClock, 1000);
setInterval(() => { void loadWeather(); }, 5 * 60 * 1000);
setInterval(() => { void loadNews(); }, 5 * 60 * 1000);
setInterval(() => { void loadFridgeState(); }, 5 * 60 * 1000);
setInterval(() => { void loadCalendarState(); }, 60 * 1000);
setInterval(() => { void loadMoodState(); }, 60 * 1000);
setInterval(() => { void loadTodoState(); }, 60 * 1000);
setInterval(() => { void loadBoardState(); }, 60 * 1000);
setInterval(() => { void loadTvApps(); }, 5 * 60 * 1000);
setInterval(() => { void loadMirrorState(); }, 30 * 1000);
setInterval(() => { void loadPowerSchedules(); }, 30 * 1000);
setInterval(() => { void loadReminders(); }, 30 * 1000);
