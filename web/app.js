const state = {
  messages: [],
  latestToolTraces: [],
  latestAssistantReply: "",
  progressItems: [],
};

const elements = {
  healthSummary: document.getElementById("health-summary"),
  heroStatusPill: document.getElementById("hero-status-pill"),
  heroStatusText: document.getElementById("hero-status-text"),
  refreshHealth: document.getElementById("refresh-health"),
  refreshAll: document.getElementById("refresh-all"),
  chatLog: document.getElementById("chat-log"),
  chatForm: document.getElementById("chat-form"),
  chatInput: document.getElementById("chat-input"),
  chatStatus: document.getElementById("chat-status"),
  clearChat: document.getElementById("clear-chat"),
  traceList: document.getElementById("trace-list"),
  itineraryMeta: document.getElementById("itinerary-meta"),
  itineraryContent: document.getElementById("itinerary-content"),
  refreshItinerary: document.getElementById("refresh-itinerary"),
  saveLatest: document.getElementById("save-latest"),
  planOverview: document.getElementById("plan-overview"),
  weatherHighlight: document.getElementById("weather-highlight"),
  sectionCards: document.getElementById("section-cards"),
  visualPicks: document.getElementById("visual-picks"),
  visualLandmark: document.getElementById("visual-landmark"),
  visualFood: document.getElementById("visual-food"),
  exampleButtons: Array.from(document.querySelectorAll(".example-chip")),
};

function escapeHtml(text) {
  return String(text ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderInlineMarkdown(text) {
  let html = escapeHtml(text);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  return html;
}

function parseTable(lines, startIndex) {
  if (startIndex + 1 >= lines.length) {
    return null;
  }

  const headerLine = lines[startIndex].trim();
  const dividerLine = lines[startIndex + 1].trim();
  if (!headerLine.includes("|") || !/^\|?\s*[:-]+[-| :]*\|?\s*$/.test(dividerLine)) {
    return null;
  }

  const rows = [];
  let endIndex = startIndex + 2;
  while (endIndex < lines.length && lines[endIndex].includes("|")) {
    rows.push(lines[endIndex]);
    endIndex += 1;
  }

  const parseCells = (line) =>
    line
      .trim()
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((cell) => renderInlineMarkdown(cell.trim()));

  return {
    html: `
      <div class="md-table-wrap">
        <table class="md-table">
          <thead><tr>${parseCells(headerLine).map((cell) => `<th>${cell}</th>`).join("")}</tr></thead>
          <tbody>${rows.map((row) => `<tr>${parseCells(row).map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody>
        </table>
      </div>
    `,
    nextIndex: endIndex,
  };
}

function markdownToHtml(markdown) {
  const lines = String(markdown || "").replace(/\r/g, "").split("\n");
  const htmlParts = [];
  let index = 0;

  while (index < lines.length) {
    const trimmed = lines[index].trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    const table = parseTable(lines, index);
    if (table) {
      htmlParts.push(table.html);
      index = table.nextIndex;
      continue;
    }

    if (/^---+$/.test(trimmed)) {
      htmlParts.push('<hr class="md-rule" />');
      index += 1;
      continue;
    }

    if (/^###\s+/.test(trimmed)) {
      htmlParts.push(`<h4>${renderInlineMarkdown(trimmed.replace(/^###\s+/, ""))}</h4>`);
      index += 1;
      continue;
    }

    if (/^##\s+/.test(trimmed)) {
      htmlParts.push(`<h3>${renderInlineMarkdown(trimmed.replace(/^##\s+/, ""))}</h3>`);
      index += 1;
      continue;
    }

    if (/^#\s+/.test(trimmed)) {
      htmlParts.push(`<h2>${renderInlineMarkdown(trimmed.replace(/^#\s+/, ""))}</h2>`);
      index += 1;
      continue;
    }

    if (/^>\s?/.test(trimmed)) {
      const quoteLines = [];
      while (index < lines.length && /^>\s?/.test(lines[index].trim())) {
        quoteLines.push(lines[index].trim().replace(/^>\s?/, ""));
        index += 1;
      }
      htmlParts.push(`<blockquote>${quoteLines.map(renderInlineMarkdown).join("<br />")}</blockquote>`);
      continue;
    }

    if (/^[-*]\s+/.test(trimmed)) {
      const items = [];
      while (index < lines.length && /^[-*]\s+/.test(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^[-*]\s+/, ""));
        index += 1;
      }
      htmlParts.push(`<ul>${items.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</ul>`);
      continue;
    }

    if (/^\d+\.\s+/.test(trimmed)) {
      const items = [];
      while (index < lines.length && /^\d+\.\s+/.test(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^\d+\.\s+/, ""));
        index += 1;
      }
      htmlParts.push(`<ol>${items.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</ol>`);
      continue;
    }

    const paragraphLines = [];
    while (index < lines.length) {
      const candidate = lines[index].trim();
      if (!candidate) {
        index += 1;
        break;
      }
      if (/^#/.test(candidate) || /^>\s?/.test(candidate) || /^[-*]\s+/.test(candidate) || /^\d+\.\s+/.test(candidate) || /^---+$/.test(candidate) || parseTable(lines, index)) {
        break;
      }
      paragraphLines.push(lines[index].trim());
      index += 1;
    }
    htmlParts.push(`<p>${renderInlineMarkdown(paragraphLines.join("<br />"))}</p>`);
  }

  return htmlParts.join("");
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    const detail = data.detail || data.message || "Request failed";
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return data;
}

function setHeroStatus(configured) {
  elements.heroStatusPill.classList.toggle("offline", !configured);
  elements.heroStatusText.textContent = configured ? "GPS Connected" : "LLM Missing";
}

function renderHealthCard(payload) {
  const data = payload?.data || {};
  const llmConfigured = Boolean(data.llm_configured);
  const amapConfigured = Boolean(data.amap_configured);
  const geoapifyConfigured = Boolean(data.geoapify_configured);

  setHeroStatus(llmConfigured);
  elements.healthSummary.innerHTML = `
    <div class="status-summary">
      <div class="status-inline ${llmConfigured ? "" : "offline"}">${llmConfigured ? "LLM 已配置，可直接规划" : "LLM 未配置，/api/chat 暂不可用"}</div>
      <div class="status-grid">
        <div class="status-tile"><span>模型名称</span><strong>${escapeHtml(data.model_name || "unknown")}</strong></div>
        <div class="status-tile"><span>高德 API</span><strong>${amapConfigured ? "已配置" : "未配置"}</strong></div>
        <div class="status-tile"><span>Geoapify</span><strong>${geoapifyConfigured ? "已配置" : "未配置"}</strong></div>
        <div class="status-tile"><span>后端状态</span><strong>在线</strong></div>
      </div>
    </div>
  `;
}

function buildAssistantPreview(message) {
  if (!message.html || message.live) {
    return null;
  }

  const reply = String(message.content || "").trim();
  if (!reply.includes("##")) {
    return null;
  }

  const sections = splitMarkdownSections(reply);
  const titleMatch = reply.match(/^#\s+(.+)$/m) || reply.match(/^##\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim() : "Plan generated";
  const sectionNames = sections
    .map((section) => section.title.trim())
    .filter((name) => name && name !== "Full reply")
    .slice(0, 4);

  return `
    <div class="assistant-preview-card">
      <div class="assistant-preview-eyebrow">Travel Plan Ready</div>
      <div class="assistant-preview-title">${escapeHtml(title)}</div>
      <div class="assistant-preview-text">A cleaner summary card is shown here. See the structured result panels below for the full itinerary.</div>
      <div class="assistant-preview-tags">
        ${sectionNames.map((name) => `<span class="assistant-preview-tag">${escapeHtml(name)}</span>`).join("")}
      </div>
    </div>
  `;
}

function createMessageNode(message) {
  const article = document.createElement("article");
  article.className = `message-bubble ${message.role}`;
  if (message.live) {
    article.classList.add("live-bubble");
  }

  const body = document.createElement("div");
  const assistantPreview = message.role === "assistant" ? buildAssistantPreview(message) : null;
  body.className = `message-body ${message.html && !assistantPreview ? "markdown-body" : ""}`;
  if (assistantPreview) {
    body.innerHTML = assistantPreview;
  } else if (message.html) {
    body.innerHTML = message.html;
  } else {
    body.textContent = message.content || "";
  }

  if (message.live) {
    const cursor = document.createElement("span");
    cursor.className = "stream-cursor";
    cursor.textContent = " ";
    body.appendChild(cursor);
  }

  article.appendChild(body);
  return article;
}

function rerenderChatLog() {
  elements.chatLog.innerHTML = "";
  if (state.messages.length === 0) {
    elements.chatLog.appendChild(createMessageNode({ role: "assistant intro-bubble", content: "TravelMate 已准备好。你可以直接输入旅行需求，或者从左侧示例开始。" }));
    return;
  }
  state.messages.forEach((message) => elements.chatLog.appendChild(createMessageNode(message)));
  elements.chatLog.scrollTop = elements.chatLog.scrollHeight;
}

function splitMarkdownSections(reply) {
  const normalized = String(reply || "").replace(/\r/g, "").trim();
  if (!normalized) {
    return [];
  }
  const lines = normalized.split("\n");
  const sections = [];
  let current = { title: "完整回复", content: [] };
  for (const line of lines) {
    const heading = line.match(/^##\s+(.+)$/);
    if (heading) {
      if (current.content.length > 0) {
        sections.push({ title: current.title, content: current.content.join("\n").trim() });
      }
      current = { title: heading[1].trim(), content: [] };
      continue;
    }
    current.content.push(line);
  }
  if (current.content.length > 0) {
    sections.push({ title: current.title, content: current.content.join("\n").trim() });
  }
  return sections;
}

function findSection(sections, keywords) {
  return sections.find((section) => keywords.some((keyword) => section.title.includes(keyword)));
}

function getToolDisplayMeta(toolName) {
  const mapping = {
    get_weather_forecast: {
      label: "Weather API - Forecast",
      hint: "Open-Meteo weather lookup",
    },
    search_attractions: {
      label: "POI API - Attractions",
      hint: "Amap live POI search",
    },
    search_local_knowledge: {
      label: "Local CSV - Knowledge Base",
      hint: "Local attractions and food dataset",
    },
    calculate_budget: {
      label: "Budget Tool - Estimate",
      hint: "Local trip budget calculator",
    },
    save_itinerary: {
      label: "Save Tool - Markdown Export",
      hint: "Save itinerary to local file",
    },
  };
  return mapping[toolName] || { label: toolName || "unknown_tool", hint: "Tool call" };
}

function renderProgressState() {
  if (state.progressItems.length === 0) {
    elements.planOverview.className = "overview-block empty-placeholder";
    elements.planOverview.textContent = "暂时还没有规划结果。发送对话后，这里会先展示实时进度，再展示结构化行程卡片。";
    return;
  }
  elements.planOverview.className = "overview-block";
  elements.planOverview.innerHTML = `
    <div class="progress-stack">
      ${state.progressItems.map((item) => `
        <div class="progress-item ${item.status}">
          <span class="progress-dot"></span>
          <div>
            <div class="progress-title">${escapeHtml(item.label)}</div>
            ${item.detail ? `<div class="progress-detail">${escapeHtml(item.detail)}</div>` : ""}
          </div>
        </div>`).join("")}
    </div>
  `;
}

function renderPlanSections(reply) {
  const sections = splitMarkdownSections(reply);
  const overview = findSection(sections, ["行程概览", "概览", "总览"]);
  const weather = findSection(sections, ["天气提醒", "天气"]);
  const landmarks = findSection(sections, ["拍照", "打卡", "景点"]);
  const foods = findSection(sections, ["美食", "餐饮"]);

  elements.planOverview.className = "overview-block markdown-body";
  elements.planOverview.innerHTML = markdownToHtml(overview?.content || sections[0]?.content || reply || "暂无内容");

  if (weather?.content) {
    elements.weatherHighlight.classList.remove("hidden");
    elements.weatherHighlight.innerHTML = `<div class="weather-icon">☀</div><div><strong>天气提醒</strong><div class="markdown-body">${markdownToHtml(weather.content)}</div></div>`;
  } else {
    elements.weatherHighlight.classList.add("hidden");
    elements.weatherHighlight.innerHTML = "";
  }

  if (landmarks?.content || foods?.content) {
    elements.visualPicks.classList.remove("hidden");
    elements.visualLandmark.textContent = (landmarks?.content || "等待地标推荐").split("\n")[0].replace(/^[-*]\s*/, "");
    elements.visualFood.textContent = (foods?.content || "等待美食推荐").split("\n")[0].replace(/^[-*]\s*/, "");
  } else {
    elements.visualPicks.classList.add("hidden");
  }

  const hiddenTitles = ["行程概览", "概览", "总览", "天气提醒", "天气"];
  const cards = sections.filter((section) => !hiddenTitles.some((title) => section.title.includes(title)));
  if (cards.length === 0) {
    elements.sectionCards.innerHTML = '<div class="empty-placeholder">Agent 回复中的各个部分会自动拆成卡片展示。</div>';
    return;
  }
  elements.sectionCards.innerHTML = cards.map((section) => `<article class="plan-section-card"><h3 class="plan-section-title">${escapeHtml(section.title)}</h3><div class="plan-section-body markdown-body">${markdownToHtml(section.content || "暂无内容")}</div></article>`).join("");
}

function renderToolTraces(traces) {
  if (!traces || traces.length === 0) {
    elements.traceList.className = "trace-list empty-placeholder";
    elements.traceList.textContent = "No tool calls yet.";
    return;
  }
  elements.traceList.className = "trace-list";
  elements.traceList.innerHTML = traces.map((trace) => {
    const meta = getToolDisplayMeta(trace.tool_name);
    return `
      <details class="trace-item">
        <summary class="trace-summary">
          <span class="trace-title-group">
            <span>${escapeHtml(meta.label)}</span>
            <span class="trace-hint">${escapeHtml(meta.hint)}</span>
          </span>
          <span class="trace-meta">
            <span class="trace-badge ${trace.success ? "success" : "fail"}">${trace.success ? "success" : "failed"}</span>
            <span>${escapeHtml(trace.result_summary || "No summary")}</span>
          </span>
        </summary>
        <div class="trace-body">
          <div class="helper-text">Tool ID</div>
          <pre>${escapeHtml(trace.tool_name || "unknown_tool")}</pre>
          <div class="helper-text">Arguments</div>
          <pre>${escapeHtml(JSON.stringify(trace.arguments || {}, null, 2))}</pre>
          <div class="helper-text">Result Preview</div>
          <pre>${escapeHtml(trace.raw_result_preview || "No preview")}</pre>
        </div>
      </details>`;
  }).join("");
}

function renderItinerary(payload) {
  const data = payload?.data || {};
  const hasContent = Boolean((data.content || "").trim());
  elements.itineraryMeta.textContent = data.path || "未找到行程文件路径。";
  elements.itineraryContent.textContent = hasContent ? "已保存 Markdown 行程。" : "当前还没有保存的行程。";
}

async function loadHealth() {
  elements.healthSummary.innerHTML = "<p>正在检查后端状态...</p>";
  try {
    renderHealthCard(await requestJson("/api/health"));
  } catch (error) {
    setHeroStatus(false);
    elements.healthSummary.innerHTML = `<div class="empty-placeholder">健康检查失败：${escapeHtml(error.message)}</div>`;
  }
}

async function loadTraces() {
  elements.traceList.className = "trace-list empty-placeholder";
  elements.traceList.textContent = "正在读取工具日志...";
  try {
    const payload = await requestJson("/api/tool-traces?limit=8");
    renderToolTraces(payload.data || []);
  } catch (error) {
    elements.traceList.className = "trace-list empty-placeholder";
    elements.traceList.textContent = `读取日志失败：${error.message}`;
  }
}

async function loadItinerary() {
  elements.itineraryMeta.textContent = "正在读取行程文件...";
  elements.itineraryContent.textContent = "正在检查保存状态...";
  try {
    renderItinerary(await requestJson("/api/itinerary"));
  } catch (error) {
    elements.itineraryMeta.textContent = "读取失败";
    elements.itineraryContent.textContent = error.message;
  }
}

function addProgressItem(label, status = "running", detail = "") {
  const item = { id: `${Date.now()}-${Math.random().toString(16).slice(2)}`, label, detail, status };
  state.progressItems.push(item);
  renderProgressState();
  return item.id;
}

function updateProgressItem(id, patch) {
  const item = state.progressItems.find((entry) => entry.id === id);
  if (!item) {
    return;
  }
  Object.assign(item, patch);
  renderProgressState();
}

function ensureAssistantMessage(index) {
  if (!state.messages[index]) {
    state.messages[index] = { role: "assistant", content: "", live: true };
  }
}

function appendAssistantDelta(index, delta) {
  ensureAssistantMessage(index);
  state.messages[index].content = (state.messages[index].content || "") + delta;
  state.messages[index].live = true;
  rerenderChatLog();
}

function finalizeAssistantMessage(index, reply) {
  ensureAssistantMessage(index);
  state.messages[index].content = reply;
  state.messages[index].live = false;
  state.messages[index].html = markdownToHtml(reply);
  rerenderChatLog();
}

async function saveLatestReply() {
  if (!state.latestAssistantReply.trim()) {
    elements.chatStatus.textContent = "当前还没有可保存的规划内容。";
    return;
  }
  try {
    const payload = await requestJson("/api/save-itinerary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "TravelMate 当前规划", content: state.latestAssistantReply }),
    });
    elements.chatStatus.textContent = payload.message || "已保存当前规划。";
    await loadItinerary();
  } catch (error) {
    elements.chatStatus.textContent = `保存失败：${error.message}`;
  }
}

async function consumeChatStream(response, assistantIndex) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalSeen = false;
  const toolProgress = new Map();

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.trim()) {
        continue;
      }
      const event = JSON.parse(line);

      if (event.type === "status") {
        addProgressItem(event.message, "running", event.stage || "");
        elements.chatStatus.textContent = event.message;
        continue;
      }
      if (event.type === "tool_start") {
        const progressId = addProgressItem(`调用工具：${event.tool_name}`, "running", JSON.stringify(event.arguments || {}));
        toolProgress.set(event.tool_name, progressId);
        continue;
      }
      if (event.type === "tool_finish") {
        const progressId = toolProgress.get(event.tool_name);
        if (progressId) {
          updateProgressItem(progressId, { status: event.trace?.success ? "done" : "failed", detail: event.summary || "" });
        }
        if (event.trace) {
          state.latestToolTraces = [...state.latestToolTraces, event.trace];
          renderToolTraces(state.latestToolTraces);
        }
        continue;
      }
      if (event.type === "token") {
        appendAssistantDelta(assistantIndex, event.delta || "");
        elements.chatStatus.textContent = "正在实时生成回答...";
        continue;
      }
      if (event.type === "final") {
        finalSeen = true;
        state.latestAssistantReply = event.reply || state.messages[assistantIndex]?.content || "";
        state.latestToolTraces = event.tool_traces || state.latestToolTraces;
        renderToolTraces(state.latestToolTraces);
        finalizeAssistantMessage(assistantIndex, state.latestAssistantReply);
        renderPlanSections(state.latestAssistantReply);
        elements.chatStatus.textContent = event.success ? "本轮规划已完成。" : "已返回结果，但 Agent 标记为失败。";
      }
    }
  }

  if (!finalSeen && state.messages[assistantIndex]?.content) {
    state.latestAssistantReply = state.messages[assistantIndex].content;
    finalizeAssistantMessage(assistantIndex, state.latestAssistantReply);
    renderPlanSections(state.latestAssistantReply);
  }
}

async function submitChat(prompt) {
  state.messages.push({ role: "user", content: prompt });
  const assistantIndex = state.messages.push({ role: "assistant", content: "", live: true }) - 1;
  state.latestToolTraces = [];
  state.latestAssistantReply = "";
  state.progressItems = [];
  rerenderChatLog();
  renderToolTraces([]);
  renderProgressState();
  elements.chatStatus.textContent = "已发送请求，正在分阶段生成结果...";

  try {
    const conversation = state.messages.slice(0, assistantIndex).filter((message) => message.role === "user" || message.role === "assistant").map(({ role, content }) => ({ role, content }));
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: conversation }),
    });
    if (!response.ok || !response.body) {
      throw new Error(`Stream request failed with status ${response.status}`);
    }
    await consumeChatStream(response, assistantIndex);
  } catch (error) {
    const message = `请求失败：${error.message}`;
    state.messages[assistantIndex] = { role: "assistant", content: message };
    rerenderChatLog();
    elements.chatStatus.textContent = "请求失败，请检查后端配置。";
    elements.planOverview.className = "overview-block empty-placeholder";
    elements.planOverview.textContent = message;
  } finally {
    await loadItinerary();
  }
}

elements.refreshHealth.addEventListener("click", loadHealth);
elements.refreshAll.addEventListener("click", async () => {
  await Promise.all([loadHealth(), loadTraces(), loadItinerary()]);
});
elements.refreshItinerary.addEventListener("click", loadItinerary);
elements.saveLatest.addEventListener("click", saveLatestReply);

elements.clearChat.addEventListener("click", () => {
  state.messages = [];
  state.latestToolTraces = [];
  state.latestAssistantReply = "";
  state.progressItems = [];
  rerenderChatLog();
  renderToolTraces([]);
  renderProgressState();
  elements.weatherHighlight.classList.add("hidden");
  elements.weatherHighlight.innerHTML = "";
  elements.visualPicks.classList.add("hidden");
  elements.sectionCards.innerHTML = '<div class="empty-placeholder">Agent 回复中的各个部分会自动拆成卡片展示。</div>';
  elements.chatStatus.textContent = "会话已清空。";
});

elements.chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const prompt = elements.chatInput.value.trim();
  if (!prompt) {
    elements.chatStatus.textContent = "请先输入内容。";
    return;
  }
  elements.chatInput.value = "";
  await submitChat(prompt);
});

elements.exampleButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const prompt = button.dataset.prompt || "";
    elements.chatInput.value = prompt;
    await submitChat(prompt);
  });
});

rerenderChatLog();
loadHealth();
loadTraces();
loadItinerary();