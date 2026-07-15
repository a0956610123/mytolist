"""收支查询模块 API"""
from flask import Blueprint, request, jsonify
from db import supabase_select, supabase_insert, supabase_update, \
    supabase_delete, supabase_rpc

finance_bp = Blueprint("finance", __name__)


SORTABLE_FIELDS = {"id", "type", "amount", "transaction_date",
                   "created_at", "updated_at"}


@finance_bp.route("/api/finance/list", methods=["GET"])
def api_finance_list():
    """获取收支列表"""
    try:
        tx_type = request.args.get("type")
        category_id = request.args.get("category_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        sort_field = request.args.get("sort", "transaction_date")
        sort_order = request.args.get("order", "desc")

        if sort_field not in SORTABLE_FIELDS:
            sort_field = "transaction_date"

        filters = []
        if tx_type and tx_type in ("income", "expense"):
            filters.append(("type", "eq.", tx_type))
        if category_id:
            filters.append(("category_id", "eq.", category_id))
        if start_date:
            filters.append(("transaction_date", "gte.", start_date))
        if end_date:
            filters.append(("transaction_date", "lte.", end_date))

        transactions = supabase_select(
            "transactions",
            columns="id,type,amount,category_id,description,transaction_date,created_at",
            filters=filters,
            order=f"{sort_field}.{sort_order}",
        )

        return jsonify({"code": 0, "data": transactions, "msg": "ok"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@finance_bp.route("/api/finance/categories", methods=["GET"])
def api_finance_categories():
    """获取收支分类列表"""
    try:
        cat_type = request.args.get("type")  # income / expense
        filters = []
        if cat_type and cat_type in ("income", "expense"):
            filters.append(("type", "eq.", cat_type))
        categories = supabase_select("categories", columns="*", filters=filters,
                                     order="id.asc")
        return jsonify({"code": 0, "data": categories, "msg": "ok"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@finance_bp.route("/api/finance/add", methods=["POST"])
def api_finance_add():
    """新增收支记录"""
    try:
        data = request.get_json(force=True)
        required = ("type", "amount", "category_id", "transaction_date")
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"code": -1, "data": None,
                            "msg": f"缺少必填字段: {', '.join(missing)}"})

        row = {
            "type": data["type"],
            "amount": float(data["amount"]),
            "category_id": int(data["category_id"]),
            "description": data.get("description", ""),
            "transaction_date": data["transaction_date"],
        }
        result = supabase_insert("transactions", row)
        return jsonify({"code": 0, "data": result[0] if result else None,
                        "msg": "新增成功"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@finance_bp.route("/api/finance/update/<int:tx_id>", methods=["PUT"])
def api_finance_update(tx_id):
    """更新收支记录"""
    try:
        data = request.get_json(force=True)
        allowed = {"type", "amount", "category_id", "description",
                   "transaction_date"}
        payload = {}
        for k in allowed:
            if k in data:
                payload[k] = data[k]
        if not payload:
            return jsonify({"code": -1, "data": None, "msg": "没有要更新的字段"})

        result = supabase_update("transactions", tx_id, payload)
        return jsonify({"code": 0, "data": result[0] if result else None,
                        "msg": "更新成功"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@finance_bp.route("/api/finance/delete/<int:tx_id>", methods=["DELETE"])
def api_finance_delete(tx_id):
    """删除收支记录"""
    try:
        supabase_delete("transactions", tx_id)
        return jsonify({"code": 0, "data": None, "msg": "删除成功"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})


@finance_bp.route("/api/finance/summary", methods=["GET"])
def api_finance_summary():
    """获取收支汇总统计（RPC）"""
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        if not start_date or not end_date:
            return jsonify({"code": -1, "data": None,
                            "msg": "请提供 start_date 和 end_date"})
        summary = supabase_rpc("get_finance_summary", {
            "p_start_date": start_date,
            "p_end_date": end_date,
        })
        return jsonify({"code": 0, "data": summary, "msg": "ok"})
    except Exception as e:
        return jsonify({"code": -1, "data": None, "msg": str(e)})
