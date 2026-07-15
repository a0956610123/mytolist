/* ===========================================================
   共用 JS — TodoList + 收支查询系统
   =========================================================== */

/* ---------- Toast 通知 ---------- */
function showToast(message, type) {
    if (type === void 0) { type = 'success'; }
    var bg = { success: '#10b981', error: '#ef4444', warning: '#f59e0b', info: '#3b82f6' };
    var container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    var id = 't-' + Date.now();
    var html = '<div id="' + id + '" class="toast align-items-center text-white border-0 show" role="alert" style="background:' + (bg[type] || bg.info) + '">' +
        '<div class="d-flex"><div class="toast-body">' + message + '</div>' +
        '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div></div>';
    container.insertAdjacentHTML('beforeend', html);
    setTimeout(function () {
        var el = document.getElementById(id);
        if (el) { el.remove(); }
    }, 3500);
}

/* ---------- 日期格式化 (本地时间 YYYY-MM-DD) ---------- */
function formatDateLocal(date) {
    var y = date.getFullYear();
    var m = String(date.getMonth() + 1).padStart(2, '0');
    var d = String(date.getDate()).padStart(2, '0');
    return y + '-' + m + '-' + d;
}

function formatDateDisplay(dateStr) {
    if (!dateStr) return '-';
    // 如果已经有 YYYY-MM-DD 格式
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return dateStr;
    var d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return formatDateLocal(d);
}

function formatDateTimeDisplay(dateStr) {
    if (!dateStr) return '-';
    var d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    var pad = function (n) { return String(n).padStart(2, '0'); };
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) +
        ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
}

/* ---------- 统一 AJAX 请求 ---------- */
function apiRequest(method, url, data, onSuccess, onError) {
    var opts = {
        url: url,
        method: method,
        contentType: 'application/json',
        dataType: 'json',
        success: function (res) {
            if (res.code === 0) {
                if (onSuccess) onSuccess(res.data, res.msg);
            } else {
                showToast(res.msg || '请求失败', 'error');
                if (onError) onError(res);
            }
        },
        error: function (xhr) {
            var msg = '网络错误';
            try { var r = JSON.parse(xhr.responseText); msg = r.msg || msg; } catch (e) {}
            showToast(msg, 'error');
            if (onError) onError(null);
        }
    };
    if (data) {
        opts.data = JSON.stringify(data);
    }
    $.ajax(opts);
}

/* ---------- 加载状态 ---------- */
function showLoading(show) {
    var el = document.getElementById('loading-overlay');
    if (show) {
        if (!el) {
            el = document.createElement('div');
            el.id = 'loading-overlay';
            el.className = 'loading-overlay';
            el.innerHTML = '<div class="spinner-custom"></div>';
            document.body.appendChild(el);
        }
        el.style.display = 'flex';
    } else {
        if (el) el.style.display = 'none';
    }
}

/* ---------- 获取本月第一/最后一天 ---------- */
function getMonthRange(offset) {
    if (offset === void 0) { offset = 0; }
    var now = new Date();
    var y = now.getFullYear();
    var m = now.getMonth() + offset;
    if (m < 0) { m = 11; y--; }
    if (m > 11) { m = 0; y++; }
    var first = new Date(y, m, 1);
    var last = new Date(y, m + 1, 0);
    return {
        start: formatDateLocal(first),
        end: formatDateLocal(last),
        year: y,
        month: m + 1
    };
}

/* ---------- 确认对话框 (Bootstrap modal) ---------- */
function confirmDialog(message, onConfirm) {
    var modal = document.getElementById('confirmModal');
    if (!modal) {
        var html = '' +
            '<div class="modal fade" id="confirmModal" tabindex="-1">' +
            '<div class="modal-dialog modal-sm modal-dialog-centered">' +
            '<div class="modal-content">' +
            '<div class="modal-body text-center py-4">' +
            '<i class="bi bi-exclamation-triangle text-warning" style="font-size:2.5rem"></i>' +
            '<p class="mt-2 mb-0" id="confirmMsg">确认？</p>' +
            '</div>' +
            '<div class="modal-footer border-0 justify-content-center pt-0">' +
            '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>' +
            '<button type="button" class="btn btn-danger" id="confirmBtn">确认删除</button>' +
            '</div></div></div></div>';
        document.body.insertAdjacentHTML('beforeend', html);
        modal = document.getElementById('confirmModal');
    }
    document.getElementById('confirmMsg').textContent = message;
    var bsModal = new bootstrap.Modal(modal);
    var btn = document.getElementById('confirmBtn');
    var newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
    newBtn.addEventListener('click', function () {
        bsModal.hide();
        if (onConfirm) onConfirm();
    });
    bsModal.show();
}
