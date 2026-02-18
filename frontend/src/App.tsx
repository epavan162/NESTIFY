import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/store/AuthContext';
import { ThemeProvider } from '@/store/ThemeContext';
import DashboardLayout from '@/layouts/DashboardLayout';
import LoginPage from '@/pages/auth/LoginPage';
import AdminDashboard from '@/pages/dashboard/AdminDashboard';
import ResidentDashboard from '@/pages/dashboard/ResidentDashboard';
import SocietyPage from '@/pages/society/SocietyPage';
import ResidentsPage from '@/pages/residents/ResidentsPage';
import MaintenancePage from '@/pages/maintenance/MaintenancePage';
import ComplaintsPage from '@/pages/complaints/ComplaintsPage';
import VisitorsPage from '@/pages/visitors/VisitorsPage';
import NoticesPage from '@/pages/notices/NoticesPage';
import BookingsPage from '@/pages/bookings/BookingsPage';
import PollsPage from '@/pages/polls/PollsPage';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const { isAuthenticated } = useAuth();
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    return <>{children}</>;
}

function DashboardRouter() {
    const { user } = useAuth();
    if (user?.role === 'admin' || user?.role === 'treasurer') return <AdminDashboard />;
    return <ResidentDashboard />;
}

function AppRoutes() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
                element={
                    <ProtectedRoute>
                        <DashboardLayout />
                    </ProtectedRoute>
                }
            >
                <Route path="/dashboard" element={<DashboardRouter />} />
                <Route path="/societies" element={<SocietyPage />} />
                <Route path="/residents" element={<ResidentsPage />} />
                <Route path="/maintenance" element={<MaintenancePage />} />
                <Route path="/complaints" element={<ComplaintsPage />} />
                <Route path="/visitors" element={<VisitorsPage />} />
                <Route path="/notices" element={<NoticesPage />} />
                <Route path="/bookings" element={<BookingsPage />} />
                <Route path="/polls" element={<PollsPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
    );
}

export default function App() {
    return (
        <ThemeProvider>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </ThemeProvider>
    );
}
