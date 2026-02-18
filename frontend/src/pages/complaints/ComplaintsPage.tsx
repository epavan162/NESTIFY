import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { MessageSquareWarning, Plus, AlertCircle, Clock, CheckCircle2 } from 'lucide-react';

export default function ComplaintsPage() {
    const { user } = useAuth();
    const [complaints, setComplaints] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showCreate, setShowCreate] = useState(false);

    useEffect(() => { fetchComplaints(); }, []);

    const fetchComplaints = () => {
        api.get('/complaints/').then(r => { setComplaints(r.data); setLoading(false); }).catch(() => setLoading(false));
    };

    const createComplaint = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            await api.post('/complaints/', {
                title: fd.get('title'), description: fd.get('description'), priority: fd.get('priority') || 'medium',
            });
            toast.success('Complaint submitted');
            setShowCreate(false);
            fetchComplaints();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const updateStatus = async (id: number, status: string) => {
        try {
            await api.put(`/complaints/${id}`, { status });
            toast.success(`Marked as ${status}`);
            fetchComplaints();
        } catch (err: any) { toast.error('Failed to update'); }
    };

    const statusBadge = (s: string) => {
        const map: Record<string, { icon: any; cls: string }> = {
            open: { icon: AlertCircle, cls: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' },
            in_progress: { icon: Clock, cls: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' },
            resolved: { icon: CheckCircle2, cls: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' },
        };
        const { icon: Icon, cls } = map[s] || map.open;
        return <span className={`px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${cls}`}><Icon className="w-3.5 h-3.5" />{s.replace('_', ' ')}</span>;
    };

    const priorityColor = (p: string) => p === 'urgent' ? 'text-red-500' : p === 'high' ? 'text-orange-500' : p === 'medium' ? 'text-amber-500' : 'text-green-500';

    if (loading) return <div className="space-y-3">{[1, 2, 3].map(i => <div key={i} className="skeleton h-20 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><MessageSquareWarning className="w-6 h-6 text-primary-500" /> Complaints</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Track and manage complaints</p>
                </div>
                <button onClick={() => setShowCreate(!showCreate)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />New Complaint</button>
            </div>

            {showCreate && (
                <motion.form onSubmit={createComplaint} className="glass-card p-6 space-y-4" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}>
                    <input name="title" placeholder="Complaint Title" className="input-field" required />
                    <textarea name="description" placeholder="Describe the issue..." className="input-field min-h-[100px]" />
                    <select name="priority" className="input-field">
                        <option value="low">Low Priority</option>
                        <option value="medium" selected>Medium Priority</option>
                        <option value="high">High Priority</option>
                        <option value="urgent">Urgent</option>
                    </select>
                    <button type="submit" className="btn-primary">Submit Complaint</button>
                </motion.form>
            )}

            <div className="space-y-3">
                {complaints.map((c, i) => (
                    <motion.div key={c.id} className="glass-card p-5" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
                        <div className="flex items-start justify-between">
                            <div className="space-y-1">
                                <h3 className="font-semibold text-surface-900 dark:text-white">{c.title}</h3>
                                <p className="text-sm text-surface-500 dark:text-gray-400">{c.description}</p>
                                <div className="flex items-center gap-3 mt-2">
                                    {statusBadge(c.status)}
                                    <span className={`text-xs font-medium ${priorityColor(c.priority)}`}>● {c.priority}</span>
                                    <span className="text-xs text-surface-400">#{c.id}</span>
                                </div>
                            </div>
                            {user?.role === 'admin' && c.status !== 'resolved' && (
                                <div className="flex gap-2">
                                    {c.status === 'open' && <button onClick={() => updateStatus(c.id, 'in_progress')} className="btn-secondary text-xs px-3 py-1">In Progress</button>}
                                    <button onClick={() => updateStatus(c.id, 'resolved')} className="btn-primary text-xs px-3 py-1">Resolve</button>
                                </div>
                            )}
                        </div>
                    </motion.div>
                ))}
                {complaints.length === 0 && <p className="text-center py-12 text-surface-400">No complaints</p>}
            </div>
        </div>
    );
}
