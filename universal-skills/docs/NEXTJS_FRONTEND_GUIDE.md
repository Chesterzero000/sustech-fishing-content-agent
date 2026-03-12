# Next.js 15 前端重构指南

> 日期：2026-03-11
> 从零开始构建现代化前端

---

## 🚀 快速开始

### 1. 创建 Next.js 15 项目

```bash
# 进入项目目录
cd 千鱼千寻3.0

# 创建 Next.js 项目
npx create-next-app@latest frontend --typescript --tailwind --app --src-dir --import-alias "@/*"

# 进入前端目录
cd frontend
```

**选项说明**：
- `--typescript`: 使用 TypeScript
- `--tailwind`: 使用 Tailwind CSS
- `--app`: 使用 App Router（Next.js 13+）
- `--src-dir`: 使用 src 目录
- `--import-alias "@/*"`: 配置路径别名

### 2. 安装核心依赖

```bash
# UI 组件库
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-tabs
npm install lucide-react  # 图标库

# 状态管理
npm install zustand

# 数据获取
npm install @tanstack/react-query axios

# 表单处理
npm install react-hook-form zod @hookform/resolvers

# 地图（钓点地图）
npm install mapbox-gl react-map-gl
npm install @types/mapbox-gl -D

# 图表（数据可视化）
npm install recharts

# 日期处理
npm install date-fns

# Supabase 客户端
npm install @supabase/supabase-js

# shadcn/ui（可选，推荐）
npx shadcn-ui@latest init
```

---

## 📁 项目结构

```
frontend/
├── src/
│   ├── app/                    # App Router 页面
│   │   ├── (auth)/            # 认证相关页面
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (main)/            # 主应用页面
│   │   │   ├── page.tsx       # 首页
│   │   │   ├── spots/         # 钓点
│   │   │   ├── catches/       # 渔获
│   │   │   ├── community/     # 钓友圈
│   │   │   └── profile/       # 个人中心
│   │   ├── layout.tsx         # 根布局
│   │   └── globals.css        # 全局样式
│   │
│   ├── components/            # 组件
│   │   ├── ui/               # UI 基础组件
│   │   ├── layout/           # 布局组件
│   │   ├── features/         # 功能组件
│   │   └── shared/           # 共享组件
│   │
│   ├── lib/                  # 工具库
│   │   ├── supabase.ts      # Supabase 客户端
│   │   ├── api.ts           # API 客户端
│   │   └── utils.ts         # 工具函数
│   │
│   ├── hooks/               # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   ├── useSpots.ts
│   │   └── useCatches.ts
│   │
│   ├── stores/              # Zustand 状态管理
│   │   ├── authStore.ts
│   │   └── uiStore.ts
│   │
│   └── types/               # TypeScript 类型
│       ├── user.ts
│       ├── spot.ts
│       └── catch.ts
│
├── public/                  # 静态资源
├── .env.local              # 环境变量
├── next.config.js          # Next.js 配置
├── tailwind.config.ts      # Tailwind 配置
└── package.json
```

---

## 🎨 核心页面实现

### 1. 首页 (`src/app/(main)/page.tsx`)

```typescript
import { Suspense } from 'react'
import { WeatherCard } from '@/components/features/WeatherCard'
import { NearbySpots } from '@/components/features/NearbySpots'
import { AICoach } from '@/components/features/AICoach'
import { TrendingPosts } from '@/components/features/TrendingPosts'

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">千鱼千寻</h1>

      {/* 天气卡片 */}
      <Suspense fallback={<WeatherSkeleton />}>
        <WeatherCard />
      </Suspense>

      {/* AI 教练 */}
      <section className="my-8">
        <h2 className="text-2xl font-semibold mb-4">AI 钓鱼教练</h2>
        <AICoach />
      </section>

      {/* 附近钓点 */}
      <section className="my-8">
        <h2 className="text-2xl font-semibold mb-4">附近钓点</h2>
        <Suspense fallback={<SpotsSkeleton />}>
          <NearbySpots />
        </Suspense>
      </section>

      {/* 热门帖子 */}
      <section className="my-8">
        <h2 className="text-2xl font-semibold mb-4">钓友圈</h2>
        <Suspense fallback={<PostsSkeleton />}>
          <TrendingPosts />
        </Suspense>
      </section>
    </div>
  )
}
```

### 2. 钓点地图 (`src/app/(main)/spots/page.tsx`)

```typescript
'use client'

import { useState } from 'react'
import Map, { Marker, Popup } from 'react-map-gl'
import { useSpots } from '@/hooks/useSpots'
import 'mapbox-gl/dist/mapbox-gl.css'

export default function SpotsPage() {
  const [viewport, setViewport] = useState({
    latitude: 22.5167,
    longitude: 113.9547,
    zoom: 12
  })
  const [selectedSpot, setSelectedSpot] = useState(null)
  const { data: spots, isLoading } = useSpots()

  return (
    <div className="h-screen">
      <Map
        {...viewport}
        onMove={evt => setViewport(evt.viewState)}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={process.env.NEXT_PUBLIC_MAPBOX_TOKEN}
      >
        {spots?.map(spot => (
          <Marker
            key={spot.id}
            latitude={spot.latitude}
            longitude={spot.longitude}
            onClick={() => setSelectedSpot(spot)}
          >
            <div className="w-8 h-8 bg-blue-500 rounded-full" />
          </Marker>
        ))}

        {selectedSpot && (
          <Popup
            latitude={selectedSpot.latitude}
            longitude={selectedSpot.longitude}
            onClose={() => setSelectedSpot(null)}
          >
            <div className="p-4">
              <h3 className="font-semibold">{selectedSpot.name}</h3>
              <p className="text-sm text-gray-600">{selectedSpot.description}</p>
            </div>
          </Popup>
        )}
      </Map>
    </div>
  )
}
```

### 3. AI 教练组件 (`src/components/features/AICoach.tsx`)

```typescript
'use client'

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { api } from '@/lib/api'

export function AICoach() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')

  const askMutation = useMutation({
    mutationFn: (q: string) => api.post('/agent', { question: q }),
    onSuccess: (data) => {
      setAnswer(data.answer)
    }
  })

  const handleAsk = () => {
    if (question.trim()) {
      askMutation.mutate(question)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-4">
        <Textarea
          placeholder="问我任何关于钓鱼的问题..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
        />
      </div>

      <Button
        onClick={handleAsk}
        disabled={askMutation.isPending}
        className="w-full"
      >
        {askMutation.isPending ? '思考中...' : '提问'}
      </Button>

      {answer && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-700">{answer}</p>
        </div>
      )}
    </div>
  )
}
```

---

## 🔧 配置文件

### 1. Supabase 客户端 (`src/lib/supabase.ts`)

```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// 类型安全的数据库查询
export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          nickname: string
          avatar_url: string
          created_at: string
        }
      }
      fishing_spots: {
        Row: {
          id: string
          name: string
          description: string
          latitude: number
          longitude: number
          rating: number
        }
      }
      // ... 其他表
    }
  }
}
```

### 2. API 客户端 (`src/lib/api.ts`)

```typescript
import axios from 'axios'

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器（添加认证）
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器（错误处理）
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
```

### 3. 认证 Hook (`src/hooks/useAuth.ts`)

```typescript
import { create } from 'zustand'
import { supabase } from '@/lib/supabase'

interface AuthState {
  user: any | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  signUp: (email: string, password: string) => Promise<void>
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  loading: true,

  signIn: async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    if (error) throw error
    set({ user: data.user })
  },

  signOut: async () => {
    await supabase.auth.signOut()
    set({ user: null })
  },

  signUp: async (email, password) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password
    })
    if (error) throw error
    set({ user: data.user })
  }
}))
```

---

## 🎨 shadcn/ui 组件

```bash
# 安装常用组件
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form
npx shadcn-ui@latest add input
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add skeleton
```

---

## 🌍 环境变量 (`.env.local`)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Mapbox
NEXT_PUBLIC_MAPBOX_TOKEN=your-mapbox-token

# Gemini (如果前端直接调用)
NEXT_PUBLIC_GEMINI_API_KEY=your-gemini-key
```

---

## 🚀 开发和部署

### 开发

```bash
# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

### 构建

```bash
# 构建生产版本
npm run build

# 本地预览
npm run start
```

### 部署到 Vercel

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
vercel --prod
```

---

## ✅ 重构检查清单

- [ ] Next.js 15 项目已创建
- [ ] 核心依赖已安装
- [ ] 项目结构已搭建
- [ ] Supabase 客户端已配置
- [ ] API 客户端已配置
- [ ] 认证系统已实现
- [ ] 首页已实现
- [ ] 钓点地图已实现
- [ ] AI 教练组件已实现
- [ ] shadcn/ui 组件已安装
- [ ] 环境变量已配置
- [ ] 开发服务器可正常运行
- [ ] 生产构建成功

---

**Next.js 15 前端重构完成！** 🎉
