import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts';
import {
    IndianRupee, AlertTriangle, Users, ShieldCheck, TrendingUp, ArrowUpRight, MessageSquareWarning, Receipt
} from 'lucide-react';

const COLORS = ['#f59e0b', '#3b82f6', '#22c55e'];

interface DashboardData {
    total_collected: number;
    total_pending: number;
    pending_count: number;
    total_complaints: number;
    open_complaints: number;
    in_progress_complaints: number;
    resolved_complaints: number;
    total_residents: number;
    active_visitors: number;
    monthly_data: { month: string; collected: number; pending: number }[];
    complaints_data: { name: string; value: number }[];
}

export default function AdminDashboard() {
    const { user } = useAuth();
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/dashboard/admin').then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false));
    }, []);

    if (loading) return <DashboardSkeleton />;
    if (!data) return <p className="text-center py-20 text-surface-500">No data available</p>;

    const stats = [
        { label: 'Total Collections', value: `₹${data.total_collected.toLocaleString()}`, icon: IndianRupee, color: 'from-emerald-500 to-green-600', shadow: 'shadow-green-500/20' },
        { label: 'Pending Dues', value: `₹${data.total_pending.toLocaleString()}`, icon: AlertTriangle, color: 'from-amber-500 to-orange-600', shadow: 'shadow-amber-500/20', sub: `${data.pending_count} invoices` },
        { label: 'Total Residents', value: data.total_residents, icon: Users, color: 'from-blue-500 to-indigo-600', shadow: 'shadow-blue-500/20' },
        { label: 'Active Visitors', value: data.active_visitors, icon: ShieldCheck, color: 'from-purple-500 to-violet-600', shadow: 'shadow-purple-500/20' },
    ];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white">Admin Dashboard</h2>
                    <p className="text-surface-500 dark:text-gray-400">Overview of your society</p>
                </div>
            </div>

            {/* Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((s, i) => (
                    <motion.div
                        key={i}
                        className="stat-card relative overflow-hidden group"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                    >
                        <div className={`absolute top-0 right-0 w-24 h-24 rounded-full bg-gradient-to-br ${s.color} opacity-10 -translate-y-6 translate-x-6 group-hover:scale-150 transition-transform duration-500`} />
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-sm text-surface-500 dark:text-gray-400">{s.label}</p>
                                <p className="text-2xl font-bold mt-1 text-surface-900 dark:text-white">{s.value}</p>
                                {s.sub && <p className="text-xs text-surface-400 mt-1">{s.sub}</p>}
                            </div>
                            <div className={`p-2.5 rounded-xl bg-gradient-to-br ${s.color} ${s.shadow} shadow-lg`}>
                                <s.icon className="w-5 h-5 text-white" />
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Monthly Bar Chart */}
                <motion.div
                    className="lg:col-span-2 glass-card p-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <h3 className="text-lg font-semibold text-surface-900 dark:text-white mb-4 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-primary-500" /> Monthly Collections
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={data.monthly_data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="text-surface-200 dark:text-surface-700" />
                            <XAxis dataKey="month" stroke="#adb5bd" fontSize={12} />
                            <YAxis stroke="#adb5bd" fontSize={12} />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(255,255,255,0.9)',
                                    borderRadius: '12px',
                                    border: 'none',
                                    boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                                }}
                            />
                            <Bar dataKey="collected" fill="#22c55e" radius={[6, 6, 0, 0]} name="Collected" />
                            <Bar dataKey="pending" fill="#f59e0b" radius={[6, 6, 0, 0]} name="Pending" />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* Complaints Pie Chart */}
                <motion.div
                    className="glass-card p-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                >
                    <h3 className="text-lg font-semibold text-surface-900 dark:text-white mb-4 flex items-center gap-2">
                        <MessageSquareWarning className="w-5 h-5 text-primary-500" /> Complaints
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie data={data.complaints_data} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value">
                                {data.complaints_data.map((_, idx) => (
                                    <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                                ))}
                            </Pie>
                            <Legend />
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </motion.div>
            </div>
        </div>
    );
}

function DashboardSkeleton() {
    return (
        <div className="space-y-6">
            <div className="skeleton h-8 w-48 rounded-lg" />
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map(i => <div key={i} className="skeleton h-28 rounded-2xl" />)}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 skeleton h-80 rounded-2xl" />
                <div className="skeleton h-80 rounded-2xl" />
            </div>
        </div>
    );
}
