import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { ShieldCheck, Plus, UserCheck, LogOut as LogOutIcon, Clock } from 'lucide-react';

export default function VisitorsPage() {
    const { user } = useAuth();
    const [visitors, setVisitors] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showCreate, setShowCreate] = useState(false);

    useEffect(() => { fetchVisitors(); }, []);
    const fetchVisitors = () => { api.get('/visitors/').then(r => { setVisitors(r.data); setLoading(false); }).catch(() => setLoading(false)); };

    const addVisitor = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            await api.post('/visitors/', {
                flat_id: Number(fd.get('flat_id')), visitor_name: fd.get('visitor_name'),
                visitor_phone: fd.get('visitor_phone'), purpose: fd.get('purpose'), vehicle_number: fd.get('vehicle_number'),
            });
            toast.success('Visitor entry added');
            setShowCreate(false);
            fetchVisitors();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const approve = async (id: number) => {
        try { await api.put(`/visitors/${id}/approve`); toast.success('Visitor approved'); fetchVisitors(); } catch { toast.error('Failed'); }
    };
    const checkout = async (id: number) => {
        try { await api.put(`/visitors/${id}/checkout`); toast.success('Visitor checked out'); fetchVisitors(); } catch { toast.error('Failed'); }
    };

    const statusColor = (s: string) => ({ pending: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300', approved: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300', rejected: 'bg-red-100 text-red-700', checked_out: 'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-gray-400' }[s] || '');

    if (loading) return <div className="space-y-3">{[1, 2, 3].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><ShieldCheck className="w-6 h-6 text-primary-500" /> Visitor Management</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Track visitors and approvals</p>
                </div>
                {['admin', 'security'].includes(user?.role || '') && (
                    <button onClick={() => setShowCreate(!showCreate)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />Add Visitor</button>
                )}
            </div>

            {showCreate && (
                <motion.form onSubmit={addVisitor} className="glass-card p-6 grid grid-cols-1 md:grid-cols-2 gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <input name="flat_id" type="number" placeholder="Flat ID" className="input-field" required />
                    <input name="visitor_name" placeholder="Visitor Name" className="input-field" required />
                    <input name="visitor_phone" placeholder="Phone Number" className="input-field" />
                    <input name="purpose" placeholder="Purpose of Visit" className="input-field" />
                    <input name="vehicle_number" placeholder="Vehicle Number (optional)" className="input-field" />
                    <button type="submit" className="btn-primary">Add Entry</button>
                </motion.form>
            )}

            <div className="space-y-3">
                {visitors.map((v, i) => (
                    <motion.div key={v.id} className="glass-card p-4 flex items-center justify-between" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-semibold text-sm">
                                {v.visitor_name.charAt(0)}
                            </div>
                            <div>
                                <p className="font-medium text-surface-900 dark:text-white">{v.visitor_name}</p>
                                <p className="text-sm text-surface-500 dark:text-gray-400">Flat #{v.flat_id} • {v.purpose || 'General visit'}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColor(v.status)}`}>{v.status}</span>
                            {v.status === 'pending' && <button onClick={() => approve(v.id)} className="btn-primary text-xs px-3 py-1.5 flex items-center gap-1"><UserCheck className="w-3.5 h-3.5" />Approve</button>}
                            {v.status === 'approved' && <button onClick={() => checkout(v.id)} className="btn-secondary text-xs px-3 py-1.5 flex items-center gap-1"><LogOutIcon className="w-3.5 h-3.5" />Checkout</button>}
                        </div>
                    </motion.div>
                ))}
                {visitors.length === 0 && <p className="text-center py-12 text-surface-400">No visitors recorded</p>}
            </div>
        </div>
    );
}
