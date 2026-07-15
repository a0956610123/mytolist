-- =============================================
-- TodoList + 收支查询系统 — Supabase 初始化 SQL
-- 请将此脚本复制到 Supabase Dashboard → SQL Editor 中执行
-- =============================================

-- 1. 待办事项表
CREATE TABLE IF NOT EXISTS todos (
    id              BIGSERIAL PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    description     TEXT DEFAULT '',
    status          VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    priority        VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    due_date        DATE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 收支分类表
CREATE TABLE IF NOT EXISTS categories (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    type            VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    icon            VARCHAR(50) DEFAULT 'bi-tag',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 收支记录表
CREATE TABLE IF NOT EXISTS transactions (
    id              BIGSERIAL PRIMARY KEY,
    type            VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    amount          DECIMAL(12,2) NOT NULL,
    category_id     BIGINT REFERENCES categories(id),
    description     TEXT DEFAULT '',
    transaction_date DATE NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- 插入分类基础数据
-- =============================================
INSERT INTO categories (name, type, icon) VALUES
    -- 收入分类
    ('工资', 'income', 'bi-cash-stack'),
    ('兼职', 'income', 'bi-briefcase'),
    ('投资收益', 'income', 'bi-graph-up-arrow'),
    ('红包', 'income', 'bi-envelope-open-heart'),
    ('其他收入', 'income', 'bi-plus-circle'),
    -- 支出分类
    ('餐饮', 'expense', 'bi-cup-hot'),
    ('交通', 'expense', 'bi-car-front'),
    ('购物', 'expense', 'bi-bag'),
    ('娱乐', 'expense', 'bi-controller'),
    ('住房', 'expense', 'bi-house'),
    ('医疗', 'expense', 'bi-heart-pulse'),
    ('教育', 'expense', 'bi-book'),
    ('通讯', 'expense', 'bi-phone'),
    ('其他支出', 'expense', 'bi-dash-circle')
ON CONFLICT DO NOTHING;

-- =============================================
-- 插入 TodoList 测试数据（20条）
-- =============================================
INSERT INTO todos (title, description, status, priority, due_date) VALUES
    ('完成项目需求文档', '编写完整的需求规格说明书，包含功能列表和用户故事', 'completed', 'high', '2026-07-10'),
    ('设计数据库表结构', '根据需求文档设计 ER 图和表结构', 'completed', 'high', '2026-07-12'),
    ('搭建 Flask 项目框架', '初始化项目结构，配置 Flask 和数据库连接', 'completed', 'medium', '2026-07-14'),
    ('实现用户注册功能', '开发用户注册页面和后端 API', 'pending', 'high', '2026-07-18'),
    ('实现用户登录功能', '开发用户登录页面和 JWT 认证', 'pending', 'high', '2026-07-19'),
    ('开发待办事项 CRUD', '实现待办事项的增删改查功能', 'pending', 'high', '2026-07-21'),
    ('开发收支记录管理', '实现收支记录的增删改查功能', 'pending', 'high', '2026-07-22'),
    ('编写单元测试', '为后端 API 编写完整的单元测试', 'pending', 'medium', '2026-07-25'),
    ('部署到服务器', '将项目部署到生产服务器', 'pending', 'high', '2026-07-30'),
    ('项目演示准备', '准备项目演示 PPT 和演示数据', 'pending', 'medium', '2026-08-01'),
    ('学习 Docker 容器化', '学习 Docker 基础知识，准备容器化部署', 'completed', 'low', '2026-07-08'),
    ('代码重构', '重构前端代码，提取公共组件', 'pending', 'medium', '2026-07-28'),
    ('数据库性能优化', '分析慢查询，添加必要索引', 'pending', 'low', '2026-07-29'),
    ('编写操作手册', '编写用户操作手册和部署文档', 'pending', 'medium', '2026-08-02'),
    ('购买服务器域名', '购买云服务器和配置域名解析', 'completed', 'low', '2026-07-05'),
    ('配置 CI/CD 流水线', '搭建 GitHub Actions 自动部署流水线', 'pending', 'medium', '2026-07-26'),
    ('UI 界面美化', '优化前端界面，统一设计风格', 'pending', 'low', '2026-08-03'),
    ('数据备份方案', '设计数据库自动备份方案', 'pending', 'low', '2026-07-27'),
    ('安全漏洞扫描', '对项目进行安全漏洞扫描和修复', 'pending', 'high', '2026-07-31'),
    ('项目总结报告', '撰写项目总结和技术复盘报告', 'pending', 'low', '2026-08-05');

-- =============================================
-- 插入收支测试数据（近3个月）
-- =============================================
-- 确定各分类 ID（动态获取，避免硬编码）
DO $$
DECLARE
    v_salary_id     BIGINT;
    v_parttime_id   BIGINT;
    v_invest_id     BIGINT;
    v_redpack_id    BIGINT;
    v_food_id       BIGINT;
    v_transport_id  BIGINT;
    v_shopping_id   BIGINT;
    v_entertain_id  BIGINT;
    v_housing_id    BIGINT;
    v_medical_id    BIGINT;
    v_edu_id        BIGINT;
    v_comm_id       BIGINT;
BEGIN
    SELECT id INTO v_salary_id FROM categories WHERE name = '工资';
    SELECT id INTO v_parttime_id FROM categories WHERE name = '兼职';
    SELECT id INTO v_invest_id FROM categories WHERE name = '投资收益';
    SELECT id INTO v_redpack_id FROM categories WHERE name = '红包';
    SELECT id INTO v_food_id FROM categories WHERE name = '餐饮';
    SELECT id INTO v_transport_id FROM categories WHERE name = '交通';
    SELECT id INTO v_shopping_id FROM categories WHERE name = '购物';
    SELECT id INTO v_entertain_id FROM categories WHERE name = '娱乐';
    SELECT id INTO v_housing_id FROM categories WHERE name = '住房';
    SELECT id INTO v_medical_id FROM categories WHERE name = '医疗';
    SELECT id INTO v_edu_id FROM categories WHERE name = '教育';
    SELECT id INTO v_comm_id FROM categories WHERE name = '通讯';

    -- 5月收支
    INSERT INTO transactions (type, amount, category_id, description, transaction_date) VALUES
        ('income', 15000.00, v_salary_id, '5月基本工资', '2026-05-10'),
        ('income', 2000.00, v_parttime_id, '周末兼职项目', '2026-05-15'),
        ('income', 500.00, v_invest_id, '基金分红', '2026-05-20'),
        ('income', 200.00, v_redpack_id, '朋友结婚红包', '2026-05-25'),
        ('expense', 2800.00, v_housing_id, '5月房租', '2026-05-01'),
        ('expense', 1200.00, v_food_id, '5月餐饮支出', '2026-05-31'),
        ('expense', 300.00, v_transport_id, '地铁月卡+打车', '2026-05-31'),
        ('expense', 800.00, v_shopping_id, '换季衣服', '2026-05-18'),
        ('expense', 400.00, v_entertain_id, '电影+聚餐', '2026-05-22'),
        ('expense', 100.00, v_comm_id, '话费充值', '2026-05-05');

    -- 6月收支
    INSERT INTO transactions (type, amount, category_id, description, transaction_date) VALUES
        ('income', 15000.00, v_salary_id, '6月基本工资', '2026-06-10'),
        ('income', 3000.00, v_parttime_id, '接了一个外包项目', '2026-06-20'),
        ('income', 600.00, v_invest_id, '股票收益', '2026-06-25'),
        ('expense', 2800.00, v_housing_id, '6月房租', '2026-06-01'),
        ('expense', 1300.00, v_food_id, '6月餐饮支出', '2026-06-30'),
        ('expense', 250.00, v_transport_id, '地铁月卡+打车', '2026-06-30'),
        ('expense', 1200.00, v_shopping_id, '618 购物节采购', '2026-06-18'),
        ('expense', 500.00, v_entertain_id, '演唱会门票', '2026-06-15'),
        ('expense', 300.00, v_medical_id, '体检费用', '2026-06-12'),
        ('expense', 200.00, v_edu_id, '在线课程', '2026-06-22'),
        ('expense', 100.00, v_comm_id, '话费充值', '2026-06-05');

    -- 7月收支
    INSERT INTO transactions (type, amount, category_id, description, transaction_date) VALUES
        ('income', 15000.00, v_salary_id, '7月基本工资', '2026-07-10'),
        ('income', 1500.00, v_parttime_id, '兼职项目尾款', '2026-07-12'),
        ('expense', 2800.00, v_housing_id, '7月房租', '2026-07-01'),
        ('expense', 600.00, v_food_id, '7月上旬餐饮', '2026-07-14'),
        ('expense', 150.00, v_transport_id, '地铁充值', '2026-07-05'),
        ('expense', 350.00, v_entertain_id, '剧本杀+聚餐', '2026-07-13'),
        ('expense', 100.00, v_comm_id, '话费充值', '2026-07-03');

END $$;

-- =============================================
-- 创建 RPC 函数：获取收支汇总统计
-- =============================================
CREATE OR REPLACE FUNCTION get_finance_summary(p_start_date DATE, p_end_date DATE)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_income DECIMAL(12,2);
    v_total_expense DECIMAL(12,2);
    v_by_category JSON;
BEGIN
    -- 总收入
    SELECT COALESCE(SUM(amount), 0) INTO v_total_income
    FROM transactions
    WHERE type = 'income'
      AND transaction_date BETWEEN p_start_date AND p_end_date;

    -- 总支出
    SELECT COALESCE(SUM(amount), 0) INTO v_total_expense
    FROM transactions
    WHERE type = 'expense'
      AND transaction_date BETWEEN p_start_date AND p_end_date;

    -- 按分类汇总
    SELECT COALESCE(json_agg(json_build_object(
        'category_id', c.id,
        'category_name', c.name,
        'type', c.type,
        'icon', c.icon,
        'total', COALESCE(t.total, 0)
    ) ORDER BY t.total DESC NULLS LAST), '[]'::json) INTO v_by_category
    FROM categories c
    LEFT JOIN (
        SELECT category_id, SUM(amount) as total
        FROM transactions
        WHERE transaction_date BETWEEN p_start_date AND p_end_date
        GROUP BY category_id
    ) t ON c.id = t.category_id;

    RETURN json_build_object(
        'total_income', v_total_income,
        'total_expense', v_total_expense,
        'balance', v_total_income - v_total_expense,
        'by_category', v_by_category
    );
END;
$$;

-- =============================================
-- 创建 RPC 函数：获取待办统计
-- =============================================
CREATE OR REPLACE FUNCTION get_todos_stats()
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_total BIGINT;
    v_completed BIGINT;
    v_pending BIGINT;
    v_high_priority BIGINT;
BEGIN
    SELECT COUNT(*) INTO v_total FROM todos;
    SELECT COUNT(*) INTO v_completed FROM todos WHERE status = 'completed';
    SELECT COUNT(*) INTO v_pending FROM todos WHERE status = 'pending';
    SELECT COUNT(*) INTO v_high_priority FROM todos WHERE status = 'pending' AND priority = 'high';

    RETURN json_build_object(
        'total', v_total,
        'completed', v_completed,
        'pending', v_pending,
        'high_priority', v_high_priority,
        'completion_rate', CASE WHEN v_total > 0 THEN ROUND(v_completed::DECIMAL / v_total * 100, 1) ELSE 0 END
    );
END;
$$;

-- =============================================
-- 启用 RLS（行级安全）并允许 anon 访问
-- =============================================
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- 允许匿名用户所有操作（因是单用户系统，暂时全开）
CREATE POLICY "Allow anon all on todos" ON todos FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow anon all on categories" ON categories FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow anon all on transactions" ON transactions FOR ALL TO anon USING (true) WITH CHECK (true);
