import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'

export default function MainLayout() {
  return (
    <div className="h-screen flex flex-col overflow-hidden bg-gray-50">
      {/* Navbar */}
      <Navbar />
      
      {/* Main Content - Full Width */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-[1600px] mx-auto px-6 pb-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
