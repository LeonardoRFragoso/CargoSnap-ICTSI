import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'

// Layout Components
import MainLayout from './components/layout/MainLayout'
import AuthLayout from './components/layout/AuthLayout'

// Pages
import Login from './pages/auth/Login'
import Dashboard from './pages/Dashboard'
import InspectionsList from './pages/inspections/InspectionsList'
import InspectionDetail from './pages/inspections/InspectionDetail'
import CreateInspectionWithWorkflow from './pages/inspections/CreateInspectionWithWorkflow'
import Profile from './pages/Profile'
import NotFound from './pages/NotFound'

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function App() {
  return (
    <Routes>
      {/* Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      {/* Protected Routes */}
      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Dashboard />} />
        <Route path="/inspections" element={<InspectionsList />} />
        <Route path="/inspections/:id" element={<InspectionDetail />} />
        <Route path="/inspections/new" element={<CreateInspectionWithWorkflow />} />
        <Route path="/profile" element={<Profile />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default App
