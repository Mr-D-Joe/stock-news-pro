import { AppProvider, useAppContext } from './context/AppContext';
import { TopBar } from '@/components/TopBar';
import { MarketOverviewCard } from '@/components/dashboard/MarketOverviewCard';
import { EventMonitorCard } from '@/components/dashboard/EventMonitorCard';
import { NewsTicker } from '@/components/dashboard/NewsTicker';
import { SummarizerCard } from '@/components/dashboard/SummarizerCard';
import { EssayCard } from '@/components/dashboard/EssayCard';
import { StatusBar } from '@/components/StatusBar';
import { Activity } from 'lucide-react';

const Dashboard = () => {
  const { uiState, analysisStatus, analysisResult } = useAppContext();
  const { selectedSector } = uiState;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-900 overflow-hidden">

      {/* 1. SECTOR & STOCK NEWS TICKERS (STACKED) */}
      {analysisResult && (
        <div className="flex flex-col border-b border-slate-800">
          {/* Upper: Sector News */}
          <div className="bg-slate-900 text-slate-200">
            <NewsTicker
              news={analysisResult.sectorNews}
              label={`${selectedSector} NEWS`}
            />
          </div>
          {/* Lower: Stock News */}
          <div className="bg-slate-800 text-white border-t border-slate-700">
            <NewsTicker
              news={analysisResult.stockNews}
              label={`${analysisResult.report.stock} NEWS`}
            />
          </div>
        </div>
      )}

      {/* 2. TOP BAR */}
      <TopBar />

      {/* 3. MAIN DASHBOARD CONTENT */}
      <main className="flex-1 overflow-y-auto p-6 md:p-8 custom-scrollbar">
        <div className="max-w-[1800px] mx-auto min-h-full">

          {/* IDLE STATE */}
          {analysisStatus === 'idle' && !analysisResult && (
            <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-6 fade-in duration-700">
              <div className="p-6 bg-white rounded-2xl shadow-sm border border-gray-100">
                <Activity className="h-10 w-10 text-blue-500" />
              </div>
              <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Financial Intelligence Dashboard</h2>
              <p className="text-slate-500 max-w-lg text-lg leading-relaxed">
                Enter a symbol (e.g. <strong>GOOG</strong>) or Sector. <br />
                Use the controls above to define Scope and Timeframe.
              </p>
            </div>
          )}

          {/* STRICT 2-COL LAYOUT */}
          {analysisResult && (
            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-12">

              {/* --- LEFT COLUMN: MARKET OVERVIEW (40-45%) --- */}
              <div className="xl:col-span-5 space-y-6">
                <MarketOverviewCard
                  executiveSummary={analysisResult.report.summary}
                  reviewData={analysisResult.report.reviewData}
                  analystRatings={analysisResult.report.analystRatings}
                  riskAssessment={analysisResult.report.riskAssessment}
                  marketSentiment={analysisResult.report.marketSentiment}
                  businessContext={analysisResult.report.businessContext}
                  generatedAt={analysisResult.report.generatedAt}
                />
              </div>

              {/* --- RIGHT COLUMN: EVENT & AI MONITOR (55-60%) --- */}
              <div className="xl:col-span-7 space-y-6">



                {/* B. PRICE CHART & MONITOR */}
                <EventMonitorCard
                  chartData={analysisResult.chartData}
                  selectedPeriod="1Y"
                  sectorNews={analysisResult.sectorNews.map((n: { title: string }) => n.title).slice(0, 5)}
                />

                {/* C. AI OUTPUTS STACKED */}
                <div className="grid grid-cols-1 gap-6">
                  <SummarizerCard
                    summary={analysisResult.report.deepAnalysis}
                    metrics={[]}
                  />
                  <EssayCard text={analysisResult.essay} />
                </div>
              </div>

            </div>
          )}
        </div>
      </main>

      <StatusBar
        statusMessage={analysisStatus === 'loading' ? "Processing Real-Time Data Stream..." : "System Operational • All Services Connected"}
        versionInfo="v3.1.0-STRICT"
      />
    </div>
  );
};

function App() {
  return (
    <AppProvider>
      <Dashboard />
    </AppProvider>
  );
}

export default App;
