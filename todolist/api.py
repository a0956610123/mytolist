"""TodoList 模块 API"""
from flask import Blueprint, request, jsonify
from db import supabase_select, supabase_insert, supabase_update, \
    supabase_delete, supabase_rpc

todolist_bp = Blueprint("todolist", __name__)


# 允许排序的字段
SORTABLE_FIELDS = {"id", "title", "status", "priority", "due_date",
                   "created_at", "updated_at"}


@todolist_bp.route("/api/todolist/list", methods=["GET"])
def api_todolist_list():
    """获取待办列表，支持筛选和排序"""
    try:
        status_filter = request.args.get("status")
        priority_filter = request.args.get("priority")
        keyword = request.args.get("keyword", "").strip()
        sort_field = request.args.get("sort", "id")
        sort_order = request.args.get("order", "desc")

        # 安全校验
        if sort_field not in SORTABLE_FIELDS:
            sort_field = "id"
        order_str = f"{sort_field}.{sort_order}"

        filters = []
        if status_filter and status_filter in ("pending", "completed"):
            filters.append(("status", "eq.", status_filter))
        if priority_filter and priority_filter in ("low", "medium", "high"):
            filters.append(("priority", "eq.", priority_filter))

        todos = supabase_select("todos", columns="*",
                                filters=filters,
                                order=order_str)

        # 关键词过滤（REST API 不好做 LIKE，取回后内存过滤）
        if keyword:
            kw = keyword.lower()
            todos = [t for t in todos
                     if kw in t.get("title", "").lower()
                     or kw in t.get("description", "").lower()]

        return jsonify({"code": 0, "data": todos, "msg": "ok"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@todolist_bp.route("/api/todolist/add", methods=["POST"])
def api_todolist_add():
    """新增待办"""
    try:
        data = request.get_json(force=True)
        if not data.get("title"):
            return jsonify({"code": -1, "data": None, "msg": "标题不能为空"})

        row = {
            "title": data["title"],
            "description": data.get("description", ""),
            "priority": data.get("priority", "medium"),
            "due_date": data.get("due_date") or None,
        }
        result = supabase_insert("todos", row)
        return jsonify({"code": 0, "data": result[0] if result else None,
                        "msg": "新增成功"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@todolist_bp.route("/api/todolist/update/<int:todo_id>", methods=["PUT"])
def api_todolist_update(todo_id):
    """更新待办"""
    try:
        data = request.get_json(force=True)
        allowed = {"title", "description", "status", "priority", "due_date"}
        payload = {k: v for k, v in data.items() if k in allowed}
        if not payload:
            return jsonify({"code": -1, "data": None, "msg": "没有要更新的字段"})

        result = supabase_update("todos", todo_id, payload)
        return jsonify({"code": 0, "data": result[0] if result else None,
                        "msg": "更新成功"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@todolist_bp.route("/api/todolist/delete/<int:todo_id>", methods=["DELETE"])
def api_todolist_delete(todo_id):
    """删除待办"""
    try:
        supabase_delete("todos", todo_id)
        return jsonify({"code": 0, "data": None, "msg": "删除成功"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@todolist_bp.route("/api/todolist/toggle/<int:todo_id>", methods=["PUT"])
def api_todolist_toggle(todo_id):
    """切换待办完成状态"""
    try:
        todo = supabase_select("todos", columns="status",
                               filters=[("id", "eq.", todo_id)])
        if not todo:
            return jsonify({"code": -1, "data": None, "msg": "待办不存在"})

        new_status = "completed" if todo[0]["status"] == "pending" else "pending"
        result = supabase_update("todos", todo_id, {"status": new_status})
        return jsonify({"code": 0, "data": result[0] if result else None,
                        "msg": "状态已切换"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@todolist_bp.route("/api/todolist/stats", methods=["GET"])
def api_todolist_stats():
    """获取待办统计（RPC）"""
    try:
        stats = supabase_rpc("get_todos_stats")
        return jsonify({"code": 0, "data": stats, "msg": "ok"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})
