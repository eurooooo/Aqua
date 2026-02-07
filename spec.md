# AI饮食助手 - 产品分析与MVP方案

## 一、产品愿景

构建一个AI驱动的智能饮食记录与推荐系统，帮助用户：

- 记录每餐饮食
- 基于饮食历史和个人情况，AI推荐下一餐食物
- 实现营养均衡，达成健康饮食目标

目标覆盖：个人健康管理、减脂/增肌辅助、医疗/营养咨询等多场景

## 二、MVP核心功能范围

### 2.1 必做功能

1. **用户信息管理**
   - 基本信息：年龄、性别、身高、体重
   - 健康目标：减重/增重/维持健康
   - 饮食限制：过敏源、偏好（素食、无麸质等）
   - 活动水平：久坐/轻度/中度/高度活跃

2. **饮食记录（AI图像识别）**
   - 拍照上传或选择图片
   - AI识别图片中的食物
   - AI分析营养成分（卡路里、蛋白质、碳水、脂肪）
   - 用户可确认/修正AI识别结果
   - 选择餐次：早餐/午餐/晚餐/加餐
   - 餐食时间记录

3. **AI推荐下一餐**
   - 输入：用户当天已吃食物、当周饮食概况、个人情况
   - 输出：推荐菜品/食谱（包含菜品名称、食材清单、营养理由）
   - 支持重新生成推荐

4. **基础数据展示**
   - 当日营养摄入概览（卡路里、蛋白质、碳水、脂肪）
   - 简单的进度条显示（对比目标值）

### 2.2 暂缓功能（后续迭代）

- 详细的营养成分分析（维生素、矿物质）
- 饮食图表和趋势分析
- 用户目标设定和进度跟踪
- 导出数据
- 用户注册/登录功能

## 三、核心数据结构

### 3.1 用户档案

```python
# Pydantic 模型（数据验证）
from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id: str  # UUID
    age: int
    gender: str  # 'male' | 'female'
    height: float  # cm
    weight: float  # kg
    goal: str  # 'lose_weight' | 'gain_weight' | 'maintain'
    activity_level: str  # 'sedentary' | 'light' | 'moderate' | 'active'
    dietary_restrictions: List[str]  # ['vegetarian', 'gluten_free', ...]
    allergies: List[str]  # ['peanuts', 'dairy', ...]
    preferences: List[str]  # ['spicy', 'mild', ...]
    target_calories: Optional[int]  # 日目标卡路里
    target_protein: Optional[float]  # 日目标蛋白质 g
    target_carbs: Optional[float]  # 日目标碳水 g
    target_fat: Optional[float]  # 日目标脂肪 g
```

### 3.2 饮食记录

```python
# 食物项模型
class FoodItem(BaseModel):
    dish_name: str
    description: Optional[str]
    calories: float
    protein: float  # g
    carbs: float  # g
    fat: float  # g
    portion: Optional[str]

# 饮食记录模型
class MealRecord(BaseModel):
    id: str  # UUID
    user_id: str  # 外键关联User
    meal_type: str  # 'breakfast' | 'lunch' | 'dinner' | 'snack'
    date: str  # YYYY-MM-DD
    timestamp: datetime
    items: List[FoodItem]
```

## 四、AI推荐逻辑

### 4.1 推荐输入

- 用户当天已吃食物（及营养总计）
- 近7天饮食历史（营养均衡性分析）
- 用户档案（目标、限制、偏好）
- 当天剩余的卡路里/营养目标

### 4.2 推荐输出

```python
# 菜品推荐模型
class RecipeSuggestion(BaseModel):
    recipe_name: str
    description: str
    calories: float
    protein: float
    carbs: float
    fat: float

# 菜品搭配方案（单套推荐）
class MealPlan(BaseModel):
    plan_name: str  # 方案名称，如"方案一"、"方案二"
    recipes: List[RecipeSuggestion]  # 这套方案包含的菜品
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    plan_reason: str  # 为什么推荐这套搭配

# 推荐结果模型（包含多套方案）
class Recommendation(BaseModel):
    meal_type: str  # 'breakfast' | 'lunch' | 'dinner' | 'snack'
    plans: List[MealPlan]  # 多套搭配方案供用户选择
```

### 4.3 推荐策略（可后续扩展）

1. **营养缺口填充**：平衡热量/碳水/蛋白质/蔬菜
2. **偏好过滤**：遵守用户的饮食限制、过敏源和口味偏好
3. **多样性保证**：避免重复推荐相同食物

## 五、技术选型建议

### 5.1 前端

- **框架**: React + TypeScript
- **构建工具**: Vite
- **UI库**: shadcn/ui
- **状态管理**: Zustand 或 React Context
- **路由**: React Router
- **图像上传**: react-dropzone 或原生 input[type="file"]

### 5.2 后端

- **框架**: Python + FastAPI
- **API风格**: RESTful
- **CORS配置**: fastapi-cors

### 5.3 数据存储

- **数据库**: SQLite（开发阶段） / PostgreSQL（生产环境）
- **ORM**: SQLAlchemy
- **理由**: 轻量级，易于部署，支持迁移到PostgreSQL

### 5.4 AI集成

**统一使用 Gemini 3 Pro**

- **图像识别 + 营养分析**: 上传食物图片，识别并分析营养成分
- **饮食推荐**: 基于饮食历史和用户档案生成菜品/食谱推荐
- **API文档**: https://ai.google.dev/gemini-api/docs

### 5.5 部署

- **前端**: Vercel
- **后端**: Render / Railway

## 六、用户流程设计

### 6.1 首次使用流程

1. 打开应用
2. 填写个人档案（基本信息 + 健康目标）
3. 系统计算每日营养目标
4. 开始记录第一餐

### 6.2 日常使用流程

1. 打开应用，查看今日已吃食物和营养进度
2. 点击"拍照记录"
3. 拍摄食物照片或上传图片
4. AI识别并分析图片中的食物
5. 用户确认/修正AI分析结果
6. 选择餐次（早餐/午餐/晚餐/加餐）
7. 保存记录
8. 点击"AI推荐下一餐"
9. 查看多套推荐方案，选择其中一套，或要求重新生成
10. 按推荐记录下一餐

## 七、技术决策确认

| 决策项       | 选择                                   |
| ------------ | -------------------------------------- |
| 用户认证     | 暂不需要登录（数据库存储）             |
| 食物数据来源 | AI图像识别 + 分析                      |
| AI推荐粒度   | 推荐菜品/食谱                          |
| 技术框架     | React + FastAPI                        |
| AI模型       | Gemini 3 Pro（统一用于图像识别和推荐） |
| 国际化       | 仅中文                                 |
| 图片存储     | 分析后即可丢弃                         |
| 数据库       | SQLite（开发）/ PostgreSQL（生产）     |

## 八、实施计划

### 8.1 项目结构

```
aqua/
├── frontend/                 # React前端
│   ├── src/
│   │   ├── components/      # UI组件
│   │   ├── pages/           # 页面
│   │   ├── services/        # API调用
│   │   ├── types/           # TypeScript类型定义
│   │   └── utils/           # 工具函数
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # FastAPI后端
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── services/        # 业务逻辑
│   │   │   ├── vision.py    # AI图像识别
│   │   │   └── recommendation.py  # AI推荐
│   │   ├── models.py        # 数据库模型
│   │   ├── database.py      # 数据库连接
│   │   └── schemas.py       # Pydantic模式
│   ├── requirements.txt
│   └── main.py
├── data/                     # SQLite数据库文件（开发环境）
└── README.md
```
