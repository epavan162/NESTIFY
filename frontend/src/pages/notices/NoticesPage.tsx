import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { Megaphone, Plus, Calendar, Tag } from 'lucide-react';

export default function NoticesPage() {
    const { user } = useAuth();
    const [notices, setNotices] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showCreate, setShowCreate] = useState(false);

    useEffect(() => { api.get('/notices/').then(r => { setNotices(r.data); setLoading(false); }).catch(() => setLoading(false)); }, []);

    const createNotice = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            await api.post('/notices/', { title: fd.get('title'), content: fd.get('content'), category: fd.get('category') || 'general' });
            toast.success('Notice posted');
            setShowCreate(false);
            api.get('/notices/').then(r => setNotices(r.data));
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const catColor = (c: string) => ({ general: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300', maintenance: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300', event: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300', emergency: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' }[c] || 'bg-surface-100 text-surface-600');

    if (loading) return <div className="space-y-3">{[1, 2, 3].map(i => <div key={i} className="skeleton h-24 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><Megaphone className="w-6 h-6 text-primary-500" /> Notice Board</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Important announcements</p>
                </div>
                {user?.role === 'admin' && <button onClick={() => setShowCreate(!showCreate)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />Post Notice</button>}
            </div>

            {showCreate && (
                <motion.form onSubmit={createNotice} className="glass-card p-6 space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <input name="title" placeholder="Notice Title" className="input-field" required />
                    <textarea name="content" placeholder="Notice content..." className="input-field min-h-[100px]" required />
                    <select name="category" className="input-field">
                        <option value="general">General</option>
                        <option value="maintenance">Maintenance</option>
                        <option value="event">Event</option>
                        <option value="emergency">Emergency</option>
                    </select>
                    <button type="submit" className="btn-primary">Publish Notice</button>
                </motion.form>
            )}

            <div className="space-y-4">
                {notices.map((n, i) => (
                    <motion.div key={n.id} className="glass-card p-6" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
                        <div className="flex items-start justify-between mb-3">
                            <h3 className="text-lg font-semibold text-surface-900 dark:text-white">{n.title}</h3>
                            <span className={`px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${catColor(n.category)}`}><Tag className="w-3 h-3" />{n.category}</span>
                        </div>
                        <p className="text-surface-600 dark:text-gray-300 leading-relaxed">{n.content}</p>
                        <div className="flex items-center gap-2 mt-4 text-xs text-surface-400">
                            <Calendar className="w-3.5 h-3.5" />{new Date(n.created_at).toLocaleDateString('en-IN', { dateStyle: 'medium' })}
                        </div>
                    </motion.div>
                ))}
                {notices.length === 0 && <p className="text-center py-12 text-surface-400">No notices posted yet</p>}
            </div>
        </div>
    );
}
