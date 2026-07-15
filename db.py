"""数据库操作层 — 通过 Supabase REST API 执行原生 SQL + 参数化查询

使用方式：
    from db import supabase_get, supabase_post, supabase_rpc
"""
import requests
from config import SUPABASE_REST_URL, SUPABASE_RPC_URL, HEADERS


# ---------------------------------------------------------------------------
# 通用请求
# ---------------------------------------------------------------------------

def _request(method, url, **kwargs):
    """发送 HTTP 请求，统一处理异常。"""
    try:
        resp = method(url, **kwargs)
        resp.raise_for_status()
        # 处理 204 No Content
        if resp.status_code == 204:
            return None
        return resp.json()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Supabase API 错误 ({resp.status_code}): {resp.text}")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("无法连接到 Supabase，请检查网络")
    except Exception as e:
        raise RuntimeError(f"请求失败: {e}")


def supabase_select(table, columns="*", filters=None, order=None,
                    range_start=None, range_end=None):
    """查询多行数据。"""
    params = {"select": columns}
    if filters:
        # filters: [(field, operator, value), ...]
        # Supabase REST API 格式: ?column=op.value  (如 ?status=eq.pending)
        for field, op, value in filters:
            params[field] = f"{op}{value}"
    if order:
        params["order"] = order

    headers = HEADERS.copy()
    if range_start is not None and range_end is not None:
        headers["Range"] = f"{range_start}-{range_end}"
        headers["Prefer"] = "count=exact"

    return _request(requests.get, SUPABASE_REST_URL + f"/{table}",
                    params=params, headers=headers)


def supabase_select_one(table, row_id, columns="*"):
    """按主键查询单行。"""
    url = f"{SUPABASE_REST_URL}/{table}?id=eq.{row_id}&select={columns}"
    data = _request(requests.get, url, headers=HEADERS)
    return data[0] if data else None


def supabase_insert(table, data):
    """插入单行 / 多行，返回插入后的数据。"""
    headers = HEADERS.copy()
    headers["Prefer"] = "return=representation"
    return _request(requests.post, SUPABASE_REST_URL + f"/{table}",
                    json=data, headers=headers)


def supabase_update(table, row_id, data):
    """按主键更新，返回更新后的数据。"""
    url = f"{SUPABASE_REST_URL}/{table}?id=eq.{row_id}"
    headers = HEADERS.copy()
    headers["Prefer"] = "return=representation"
    return _request(requests.patch, url, json=data, headers=headers)


def supabase_delete(table, row_id):
    """按主键删除。"""
    url = f"{SUPABASE_REST_URL}/{table}?id=eq.{row_id}"
    _request(requests.delete, url, headers=HEADERS)
    return True


def supabase_rpc(func_name, params=None):
    """调用 RPC 函数（PostgreSQL 函数）。"""
    return _request(requests.post, SUPABASE_RPC_URL + f"/{func_name}",
                    json=params or {}, headers=HEADERS)
