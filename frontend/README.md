# CPGrams Trends Frontend

Modern Next.js dashboard application with Tremor components for interactive charts and analytics.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm

### Installation

1. Install dependencies:

```bash
pnpm install
# or
npm install --legacy-peer-deps
```

2. Start development server:

```bash
pnpm dev
# or
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📊 Features

### Dashboard Components

- **KPI Cards** - Key performance indicators with trend indicators
- **Sales Chart** - Area chart showing sales and profit over time
- **Analytics Donut Chart** - Department distribution visualization
- **Time Series Chart** - Website traffic over time
- **Revenue Bar Chart** - Monthly revenue vs profit comparison

### Technical Features

- **Real-time Data** - Fetches live data from FastAPI backend
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Loading States** - Skeleton loading for better UX
- **Error Handling** - Graceful error handling with retry options
- **TypeScript** - Full type safety throughout the application

## 🛠️ Technology Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety and better developer experience
- **Tremor** - Beautiful chart and dashboard components
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Modern icon library

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Dashboard page
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── KPICards.tsx        # KPI card components
│   │   ├── SalesChart.tsx      # Sales area chart
│   │   ├── AnalyticsDonutChart.tsx # Donut chart
│   │   ├── TimeSeriesChart.tsx # Line chart
│   │   └── RevenueBarChart.tsx # Bar chart
│   ├── lib/
│   │   └── api.ts              # API utilities
│   └── types/
│       └── chart-types.ts      # TypeScript definitions
├── package.json                # Dependencies
└── README.md                  # This file
```

## 🔧 Development

### Environment Variables

Create a `.env.local` file for local development:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Available Scripts

```bash
# Development
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Linting
pnpm lint

# Type checking
pnpm type-check
```

## 📈 Chart Components

### Using Tremor Components

This project uses [Tremor](https://github.com/tremorlabs/tremor) for chart components:

- `AreaChart` - For sales performance visualization
- `DonutChart` - For department distribution
- `LineChart` - For time series data
- `BarChart` - For revenue comparisons
- `Card` & `KPICard` - For metrics display

### Adding New Charts

1. Create a new component in `src/components/`
2. Define the data type in `src/types/chart-types.ts`
3. Add API endpoint in `src/lib/api.ts`
4. Import and use in `src/app/page.tsx`

## 🎨 Styling

The application uses Tailwind CSS for styling with Tremor's design system:

- **Colors**: Tremor color palette (blue, emerald, red, amber, etc.)
- **Layout**: Responsive grid system
- **Components**: Tremor's pre-built components
- **Custom Styles**: Minimal custom CSS

## 🔌 API Integration

The frontend connects to the FastAPI backend:

- **Base URL**: `http://localhost:8000`
- **Error Handling**: Graceful fallbacks and retry options
- **Type Safety**: Full TypeScript support for API responses

### API Endpoints Used

- `GET /api/health` - Health check
- `GET /api/charts/kpi-cards` - KPI data
- `GET /api/charts/sales` - Sales data
- `GET /api/charts/donut-data` - Donut chart data
- `GET /api/charts/time-series` - Time series data
- `GET /api/charts/revenue-by-month` - Revenue data

## 🧪 Testing

```bash
# Run tests (when available)
pnpm test

# Run e2e tests (when available)
pnpm test:e2e
```

## 📦 Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Connect to Vercel
3. Set environment variables
4. Deploy

### Docker

```bash
# Build image
docker build -t cpgrams-frontend .

# Run container
docker run -p 3000:3000 cpgrams-frontend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with backend running
5. Submit a pull request
