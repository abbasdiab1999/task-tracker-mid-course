const api = "";
const statuses = ["ToDo", "InProgress", "Done"];
const priorityOrder = {High: 0, Medium: 1, Low: 2};
const statusLabels = {ToDo: "To Do", InProgress: "In Progress", Done: "Done"};

const elements = {
  createForm: document.querySelector("#create-form"),
  formError: document.querySelector("#form-error"),
  filters: {
    status: document.querySelector("#filter-status"),
    priority: document.querySelector("#filter-priority"),
    overdue: document.querySelector("#filter-overdue"),
    tag: document.querySelector("#filter-tag"),
  },
  boardCounts: {
    ToDo: document.querySelector("#count-ToDo"),
    InProgress: document.querySelector("#count-InProgress"),
    Done: document.querySelector("#count-Done"),
  },
  boardBodies: {
    ToDo: document.querySelector("#ToDo"),
    InProgress: document.querySelector("#InProgress"),
    Done: document.querySelector("#Done"),
  },
  totalCount: document.querySelector("#total-count"),
  overdueCount: document.querySelector("#overdue-count"),
  emptyState: document.querySelector("#empty-state"),
  resultsNote: document.querySelector("#results-note"),
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[character]);
}

function parseTags(text) {
  return text.split(",").map(item => item.trim()).filter(Boolean);
}

function nextStatus(current) {
  if (current === "ToDo") return "InProgress";
  if (current === "InProgress") return "Done";
  return "InProgress";
}

function buildTaskQuery() {
  const params = new URLSearchParams();
  const status = elements.filters.status.value;
  const priority = elements.filters.priority.value;
  const overdue = elements.filters.overdue.value;
  const tag = elements.filters.tag.value.trim();

  if (status) params.set("status", status);
  if (priority) params.set("priority", priority);
  if (overdue) params.set("overdue", overdue);
  if (tag) params.set("tag", tag);

  const query = params.toString();
  return query ? `?${query}` : "";
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: {"Content-Type": "application/json", ...(options.headers || {})},
    ...options,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      detail = Array.isArray(body.detail)
        ? body.detail.map(item => item.msg).join("; ")
        : (body.detail || detail);
    } catch (_) {
      // Fall back to the generic HTTP status message.
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

async function moveTask(id, current) {
  try {
    await request(`${api}/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify({status: nextStatus(current)}),
    });
    await loadTasks();
  } catch (error) {
    alert(error.message);
    await loadTasks();
  }
}

async function deleteTask(id) {
  await request(`${api}/tasks/${id}`, {method: "DELETE"});
  await loadTasks();
}

function createEmptyCard(message) {
  const empty = document.createElement("div");
  empty.className = "empty-card";
  empty.textContent = message;
  return empty;
}

function renderTask(task) {
  const card = document.createElement("article");
  card.className = `card${task.overdue ? " overdue" : ""}`;

  const dueSection = task.due_date
    ? `<div class="meta-row"><span class="meta-label">Due</span><span>${escapeHtml(task.due_date)}</span>${task.overdue ? '<span class="pill warning">Overdue</span>' : ""}</div>`
    : "";

  const assigneeSection = task.assignee
    ? `<div class="meta-row"><span class="meta-label">Assignee</span><span>${escapeHtml(task.assignee)}</span></div>`
    : "";

  const tags = task.tags.length
    ? task.tags.map(tag => `<span class="pill">${escapeHtml(tag)}</span>`).join("")
    : '<span class="muted">No tags</span>';

  card.innerHTML = `
    <div class="card-top">
      <span class="status-chip">${statusLabels[task.status] || task.status}</span>
      <span class="priority priority-${task.priority.toLowerCase()}">${escapeHtml(task.priority)}</span>
    </div>
    <h3>${escapeHtml(task.title)}</h3>
    <p>${escapeHtml(task.description || "No description provided.")}</p>
    <div class="details">
      ${assigneeSection}
      ${dueSection}
      <div class="tag-row">${tags}</div>
    </div>
    <div class="actions">
      <button class="move" type="button">Move to ${statusLabels[nextStatus(task.status)]}</button>
      <button class="delete danger" type="button">Delete</button>
    </div>
  `;

  card.querySelector(".move").onclick = () => moveTask(task.id, task.status);
  card.querySelector(".delete").onclick = () => deleteTask(task.id);
  return card;
}

function updateMetrics(tasks) {
  const total = tasks.length;
  const overdueCount = tasks.filter(task => task.overdue).length;
  elements.totalCount.textContent = String(total);
  elements.overdueCount.textContent = String(overdueCount);
}

function clearBoard() {
  statuses.forEach(status => {
    elements.boardBodies[status].innerHTML = "";
    elements.boardCounts[status].textContent = "0";
  });
}

async function loadTasks() {
  const query = buildTaskQuery();
  const tasks = await request(`${api}/tasks${query}`);

  clearBoard();
  updateMetrics(tasks);

  const sortedTasks = [...tasks].sort((left, right) => {
    const statusDelta = statuses.indexOf(left.status) - statuses.indexOf(right.status);
    if (statusDelta !== 0) return statusDelta;
    return priorityOrder[left.priority] - priorityOrder[right.priority];
  });

  sortedTasks.forEach(task => {
    elements.boardBodies[task.status].appendChild(renderTask(task));
    elements.boardCounts[task.status].textContent = String(
      Number(elements.boardCounts[task.status].textContent) + 1
    );
  });

  const isFiltered = Boolean(query);
  elements.emptyState.hidden = tasks.length > 0 || isFiltered;
  if (!isFiltered) {
    elements.emptyState.innerHTML = "";
  }

  if (tasks.length === 0 && !isFiltered) {
    elements.emptyState.replaceChildren(
      createEmptyCard("No tasks yet. Add one to populate the board.")
    );
  }

  const noteParts = [];
  if (elements.filters.status.value) noteParts.push(`Status: ${statusLabels[elements.filters.status.value]}`);
  if (elements.filters.priority.value) noteParts.push(`Priority: ${elements.filters.priority.value}`);
  if (elements.filters.overdue.value) noteParts.push(elements.filters.overdue.value === "true" ? "Overdue only" : "Not overdue");
  if (elements.filters.tag.value.trim()) noteParts.push(`Tag: ${elements.filters.tag.value.trim()}`);
  elements.resultsNote.textContent = noteParts.length ? noteParts.join(" · ") : "Showing all tasks";
}

elements.createForm.addEventListener("submit", async event => {
  event.preventDefault();
  elements.formError.textContent = "";

  const payload = {
    title: document.querySelector("#title").value,
    description: document.querySelector("#description").value,
    priority: document.querySelector("#priority").value,
    assignee: document.querySelector("#assignee").value || null,
    due_date: document.querySelector("#due-date").value || null,
    tags: parseTags(document.querySelector("#tags").value),
  };

  try {
    await request(`${api}/tasks`, {method: "POST", body: JSON.stringify(payload)});
    event.target.reset();
    document.querySelector("#priority").value = "Medium";
    await loadTasks();
  } catch (error) {
    elements.formError.textContent = error.message;
  }
});

document.querySelector("#apply-filters").addEventListener("click", loadTasks);
document.querySelector("#clear-filters").addEventListener("click", () => {
  Object.values(elements.filters).forEach(field => {
    field.value = "";
  });
  loadTasks();
});

loadTasks();
