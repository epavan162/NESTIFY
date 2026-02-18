import { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import { useTheme } from '@/store/ThemeContext';
import {
    LayoutDashboard, Building2, Users, Receipt, MessageSquareWarning,
    ShieldCheck, Megaphone, CalendarDays, Vote, LogOut, Menu, X,
    Sun, Moon, ChevronLeft, Home,
} from 'lucide-react';

const adminNav = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/societies', icon: Building2, label: 'Society' },
    { to: '/residents', icon: Users, label: 'Residents' },
    { to: '/maintenance', icon: Receipt, label: 'Maintenance' },
    { to: '/complaints', icon: MessageSquareWarning, label: 'Complaints' },
    { to: '/visitors', icon: ShieldCheck, label: 'Visitors' },
    { to: '/notices', icon: Megaphone, label: 'Notices' },
    { to: '/bookings', icon: CalendarDays, label: 'Bookings' },
    { to: '/polls', icon: Vote, label: 'Polls' },
];

const residentNav = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/maintenance', icon: Receipt, label: 'My Bills' },
    { to: '/complaints', icon: MessageSquareWarning, label: 'Complaints' },
    { to: '/visitors', icon: ShieldCheck, label: 'Visitors' },
    { to: '/notices', icon: Megaphone, label: 'Notices' },
    { to: '/bookings', icon: CalendarDays, label: 'Bookings' },
    { to: '/polls', icon: Vote, label: 'Polls' },
];

const securityNav = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/visitors', icon: ShieldCheck, label: 'Visitors' },
];

export default function DashboardLayout() {
    const { user, logout } = useAuth();
    const { isDark, toggle } = useTheme();
    const navigate = useNavigate();
    const [collapsed, setCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    const navItems = user?.role === 'admin' ? adminNav
        : user?.role === 'security' ? securityNav
            : residentNav;

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const sidebarWidth = collapsed ? 'w-20' : 'w-64';

    return (
        <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-[#0f1019]">
            {/* Mobile Overlay */}
            <AnimatePresence>
                {mobileOpen && (
                    <motion.div
                        className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setMobileOpen(false)}
                    />
                )}
            </AnimatePresence>

            {/* Sidebar */}
            <motion.aside
                className={`fixed lg:relative z-50 h-full ${sidebarWidth} bg-white dark:bg-[#141422] border-r border-surface-100 dark:border-surface-800 flex flex-col transition-all duration-300 ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
                    }`}
                layout
            >
                {/* Logo */}
                <div className="flex items-center justify-between p-4 border-b border-surface-100 dark:border-surface-800">
                    <motion.div className="flex items-center gap-3" layout>
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/30">
                            <Home className="w-5 h-5 text-white" />
                        </div>
                        <AnimatePresence>
                            {!collapsed && (
                                <motion.span
                                    className="font-bold text-xl gradient-text"
                                    initial={{ opacity: 0, width: 0 }}
                                    animate={{ opacity: 1, width: 'auto' }}
                                    exit={{ opacity: 0, width: 0 }}
                                >
                                    Nestify
                                </motion.span>
                            )}
                        </AnimatePresence>
                    </motion.div>
                    <button
                        onClick={() => setCollapsed(!collapsed)}
                        className="hidden lg:flex p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
                    >
                        <ChevronLeft className={`w-4 h-4 text-surface-500 transition-transform duration-300 ${collapsed ? 'rotate-180' : ''}`} />
                    </button>
                </div>

                {/* Navigation */}
                <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            onClick={() => setMobileOpen(false)}
                            className={({ isActive }) =>
                                `sidebar-item ${isActive ? 'active' : ''}`
                            }
                        >
                            <item.icon className="w-5 h-5 shrink-0" />
                            <AnimatePresence>
                                {!collapsed && (
                                    <motion.span
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        exit={{ opacity: 0 }}
                                        className="whitespace-nowrap"
                                    >
                                        {item.label}
                                    </motion.span>
                                )}
                            </AnimatePresence>
                        </NavLink>
                    ))}
                </nav>

                {/* Footer */}
                <div className="p-3 border-t border-surface-100 dark:border-surface-800 space-y-1">
                    <button onClick={toggle} className="sidebar-item w-full">
                        {isDark ? <Sun className="w-5 h-5 shrink-0" /> : <Moon className="w-5 h-5 shrink-0" />}
                        {!collapsed && <span>{isDark ? 'Light Mode' : 'Dark Mode'}</span>}
                    </button>
                    <button onClick={handleLogout} className="sidebar-item w-full text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-500/10">
                        <LogOut className="w-5 h-5 shrink-0" />
                        {!collapsed && <span>Logout</span>}
                    </button>
                </div>
            </motion.aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <header className="h-16 bg-white/80 dark:bg-[#141422]/80 backdrop-blur-xl border-b border-surface-100 dark:border-surface-800 flex items-center justify-between px-4 lg:px-6">
                    <div className="flex items-center gap-3">
                        <button onClick={() => setMobileOpen(true)} className="lg:hidden p-2 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800">
                            <Menu className="w-5 h-5" />
                        </button>
                        <h1 className="text-lg font-semibold text-surface-800 dark:text-gray-100">
                            Welcome back, <span className="gradient-text">{user?.name || 'User'}</span>
                        </h1>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 capitalize">
                            {user?.role}
                        </span>
                        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-semibold text-sm">
                            {user?.name?.charAt(0) || 'U'}
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto p-4 lg:p-6">
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                    >
                        <Outlet />
                    </motion.div>
                </main>
            </div>
        </div>
    );
}
