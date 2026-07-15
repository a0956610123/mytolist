# TodoList + 收支查询系统

一个基于 Flask + Supabase + Bootstrap 5 的全栈 Web 应用，集成待办事项管理和个人收支查询两大核心功能。

## ✨ 功能特性

### 📋 待办事项管理
- ✅ 完整的 CRUD 操作（新增、编辑、删除、查看）
- 🎯 优先级标记（高/中/低）
- 📅 截止日期设置
- ✔️ 一键切换完成状态
- 🔍 关键词搜索、状态筛选、优先级筛选
- 📊 统计面板（总数、已完成、待完成、完成率）

### 💰 收支查询
- 💳 收支记录管理（收入/支出）
- 🏷️ 14 种预置分类（工资、餐饮、交通、购物等）
- 📈 实时汇总统计（总收入、总支出、结余）
- 📊 分类排行榜（Top 5）
- 📆 日期范围筛选
- 🎨 分类图标展示（Bootstrap Icons）

### 🏠 仪表盘
- 📌 待办概览（总数、完成数、高优先级提醒）
- 💵 本月财务概览（收入、支出、结余）
- 🔗 快捷入口导航

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | Python 3.9+ / Flask 3.x |
| **数据库** | Supabase (PostgreSQL) - REST API |
| **前端** | jQuery 3.7 / Bootstrap 5.3 / JavaScript |
| **图标** | Bootstrap Icons 1.11 |
| **样式** | CSS3 + 响应式设计 |

## 📁 项目结构

```
project_03_todolist/
├── app.py                      # Flask 应用入口
├── config.py                   # Supabase 配置
├── db.py                       # 数据库操作层（REST API 封装）
├── requirements.txt            # Python 依赖
├── .gitignore                  # Git 忽略文件
│
├── static/
│   ├── common.js               # 公共 JS（Toast、AJAX、日期格式化、确认框）
│   └── common.css              # 公共 CSS（侧边栏、卡片、表格、响应式）
│
├── templates/
│   ├── layout.html             # 基础布局模板（侧边栏 + 顶栏）
│   ├── index.html              # 仪表盘页面
│   ├── todolist.html           # 待办事项页面
│   └── finance.html            # 收支查询页面
│
├── todolist/
│   └── api.py                  # 待办事项 API（5 个端点）
│
├── finance/
│   └── api.py                  # 收支查询 API（6 个端点）
│
└── doc/
    └── supabase-init.sql       # 数据库初始化脚本
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/a0956610123/mytolist.git
cd mytolist

# 安装依赖（推荐使用虚拟环境）
pip install -r requirements.txt
```

### 2. 配置 Supabase

1. 注册 [Supabase](https://supabase.com/) 账号并创建项目
2. 在 Supabase Dashboard → SQL Editor 中执行 `doc/supabase-init.sql`
3. 获取项目的 API URL 和 anon key
4. 修改 `config.py` 中的配置：

```python
SUPABASE_URL = "https://你的项目ID.supabase.co"
SUPABASE_KEY = "你的anon_key"
```

或创建 `.env` 文件：

```env
SUPABASE_URL=https://你的项目ID.supabase.co
SUPABASE_KEY=你的anon_key
```

### 3. 启动应用

```bash
python app.py
```

访问 `http://localhost:5000` 即可使用。

## 📡 API 文档

### TodoList 模块

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/api/todolist/list` | 获取待办列表（支持筛选） |
| POST | `/api/todolist/add` | 新增待办 |
| PUT | `/api/todolist/update/<id>` | 更新待办 |
| DELETE | `/api/todolist/delete/<id>` | 删除待办 |
| PUT | `/api/todolist/toggle/<id>` | 切换完成状态 |
| GET | `/api/todolist/stats` | 获取统计数据（RPC） |

### 收支查询模块

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/api/finance/list` | 获取收支列表（支持筛选） |
| POST | `/api/finance/add` | 新增收支记录 |
| PUT | `/api/finance/update/<id>` | 更新收支记录 |
| DELETE | `/api/finance/delete/<id>` | 删除收支记录 |
| GET | `/api/finance/categories` | 获取分类列表 |
| GET | `/api/finance/summary` | 获取汇总统计（RPC） |

### 请求/响应格式

**请求示例（新增待办）：**
```json
POST /api/todolist/add
Content-Type: application/json

{
  "title": "完成项目文档",
  "description": "编写完整的 README",
  "priority": "high",
  "due_date": "2026-07-20"
}
```

**响应格式：**
```json
{
  "code": 0,
  "data": { ... },
  "msg": "新增成功"
}
```

## 🗄️ 数据库设计

### 表结构

#### todos - 待办事项
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键 |
| title | VARCHAR(200) | 标题 |
| description | TEXT | 描述 |
| status | VARCHAR(20) | 状态（pending/completed） |
| priority | VARCHAR(10) | 优先级（low/medium/high） |
| due_date | DATE | 截止日期 |
| created_at | TIMESTAMPTZ | 创建时间 |
| updated_at | TIMESTAMPTZ | 更新时间 |

#### categories - 收支分类
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键 |
| name | VARCHAR(100) | 分类名称 |
| type | VARCHAR(10) | 类型（income/expense） |
| icon | VARCHAR(50) | 图标类名 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### transactions - 收支记录
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键 |
| type | VARCHAR(10) | 类型（income/expense） |
| amount | DECIMAL(12,2) | 金额 |
| category_id | BIGINT | 分类 ID（外键） |
| description | TEXT | 描述 |
| transaction_date | DATE | 交易日期 |
| created_at | TIMESTAMPTZ | 创建时间 |
| updated_at | TIMESTAMPTZ | 更新时间 |

### RPC 函数

- `get_todos_stats()` - 获取待办统计（总数、完成数、完成率等）
- `get_finance_summary(start_date, end_date)` - 获取收支汇总（总收入、总支出、按分类汇总）

## 🎨 界面预览

- **侧边栏导航** - 深蓝渐变主题，清晰的图标导航
- **响应式设计** - 支持桌面端和移动端自适应
- **Material 风格** - 卡片式布局，阴影效果，流畅动画
- **Toast 通知** - 操作反馈提示
- **模态框** - 新增/编辑表单弹窗

## 🔐 安全说明

- 使用 Supabase Row Level Security (RLS) 进行数据访问控制
- 所有数据库操作使用参数化查询，防止 SQL 注入
- 前端表单验证 + 后端数据校验

## 📝 开发规范

- API 命名规则：`api_模块名_功能`
- 禁止使用 SQLAlchemy / Flask-SQLAlchemy
- 所有数据库操作使用原生 SQL + Supabase REST API
- JavaScript 共用代码放在 `static/common.js`
- CSS 共用样式放在 `static/common.css`
- 前后端通信使用 JSON 格式

## 📦 依赖清单

```txt
flask==3.1.0
requests==2.32.3
python-dotenv==1.1.0
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

## 👤 作者

**sam cheng**
- GitHub: [@a0956610123](https://github.com/a0956610123)

---

⭐ 如果这个项目对你有帮助，欢迎 Star！
