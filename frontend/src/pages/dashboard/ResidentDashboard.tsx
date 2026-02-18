import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { IndianRupee, Receipt, MessageSquareWarning, Megaphone } from 'lucide-react';

export default function ResidentDashboard() {
    const { user } = useAuth();
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => { api.get('/dashboard/resident').then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false)); }, []);

    if (loading) return <div className="space-y-4">{[1, 2, 3, 4].map(i => <div key={i} className="skeleton h-24 rounded-xl" />)}</div>;
    if (!data) return <p className="text-center py-20 text-surface-500">No data</p>;

    const stats = [
        { label: 'Pending Amount', value: `₹${data.pending_amount.toLocaleString()}`, icon: IndianRupee, color: 'from-amber-500 to-orange-600' },
        { label: 'Total Paid', value: `₹${data.total_paid.toLocaleString()}`, icon: Receipt, color: 'from-emerald-500 to-green-600' },
        { label: 'Pending Bills', value: data.pending_bills, icon: Receipt, color: 'from-blue-500 to-indigo-600' },
        { label: 'Open Complaints', value: data.open_complaints, icon: MessageSquareWarning, color: 'from-red-500 to-pink-600' },
    ];

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-surface-900 dark:text-white">My Dashboard</h2>
                <p className="text-surface-500 dark:text-gray-400">Welcome, {user?.name}</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((s, i) => (
                    <motion.div key={i} className="stat-card relative overflow-hidden" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
                        <div className={`absolute top-0 right-0 w-20 h-20 rounded-full bg-gradient-to-br ${s.color} opacity-10 -translate-y-4 translate-x-4`} />
                        <p className="text-sm text-surface-500 dark:text-gray-400">{s.label}</p>
                        <p className="text-2xl font-bold mt-1 text-surface-900 dark:text-white">{s.value}</p>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <motion.div className="glass-card p-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}>
                    <h3 className="font-semibold text-surface-900 dark:text-white mb-4 flex items-center gap-2"><Receipt className="w-5 h-5 text-primary-500" />Recent Invoices</h3>
                    <div className="space-y-3">
                        {(data.recent_invoices || []).map((inv: any) => (
                            <div key={inv.id} className="flex items-center justify-between p-3 rounded-xl bg-surface-50 dark:bg-surface-800">
                                <div><p className="font-medium text-surface-900 dark:text-white">{inv.month}/{inv.year}</p></div>
                                <div className="flex items-center gap-2">
                                    <span className="font-semibold">₹{inv.amount}</span>
                                    <span className={`px-2 py-0.5 text-xs rounded-full ${inv.status === 'paid' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>{inv.status}</span>
                                </div>
                            </div>
                        ))}
                        {(!data.recent_invoices || data.recent_invoices.length === 0) && <p className="text-sm text-surface-400 text-center py-4">No invoices</p>}
                    </div>
                </motion.div>

                <motion.div className="glass-card p-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}>
                    <h3 className="font-semibold text-surface-900 dark:text-white mb-4 flex items-center gap-2"><MessageSquareWarning className="w-5 h-5 text-primary-500" />Recent Complaints</h3>
                    <div className="space-y-3">
                        {(data.recent_complaints || []).map((c: any) => (
                            <div key={c.id} className="flex items-center justify-between p-3 rounded-xl bg-surface-50 dark:bg-surface-800">
                                <p className="font-medium text-surface-900 dark:text-white truncate flex-1">{c.title}</p>
                                <span className={`px-2 py-0.5 text-xs rounded-full ml-2 ${c.status === 'resolved' ? 'bg-green-100 text-green-700' : c.status === 'in_progress' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'}`}>{c.status}</span>
                            </div>
                        ))}
                        {(!data.recent_complaints || data.recent_complaints.length === 0) && <p className="text-sm text-surface-400 text-center py-4">No complaints</p>}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
