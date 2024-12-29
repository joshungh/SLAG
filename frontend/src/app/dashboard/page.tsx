import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#0a0f14] text-green-400 font-['VT323']">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Header />
        <main className="mt-12 space-y-16">
          <section className="border border-green-500 rounded-lg overflow-hidden">
            <div className="bg-gray-800 text-green-400 px-4 py-2 font-bold text-sm">
              &gt; SLAG Story Engine Dashboard
            </div>
            <div className="bg-black p-6">
              <p className="text-green-400 font-['IBM_Plex_Mono'] text-sm">
                &gt; Dashboard under construction...
              </p>
            </div>
          </section>
        </main>
        <Footer />
      </div>
    </div>
  )
} 