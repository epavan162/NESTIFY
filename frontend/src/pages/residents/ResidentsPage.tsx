import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import api from '@/api/client';
import { toast } from 'sonner';
import { Users, UserPlus, Home, UserX } from 'lucide-react';

export default function ResidentsPage() {
    const [residents, setResidents] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => { api.get('/residents/').then(r => { setResidents(r.data); setLoading(false); }).catch(() => setLoading(false)); }, []);

    const moveOut = async (id: number) => {
        try { await api.post(`/residents/${id}/move-out`); toast.success('Resident moved out'); api.get('/residents/').then(r => setResidents(r.data)); } catch { toast.error('Failed'); }
    };

    if (loading) return <div className="space-y-3">{[1, 2, 3].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><Users className="w-6 h-6 text-primary-500" /> Resident Management</h2>
                <p className="text-surface-500 dark:text-gray-400 text-sm">Manage residents and flat assignments</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {residents.map((r, i) => (
                    <motion.div key={r.id} className="glass-card p-5" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
                        <div className="flex items-start gap-4">
                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-bold text-lg shrink-0">
                                {r.name.charAt(0)}
                            </div>
                            <div className="flex-1 min-w-0">
                                <h3 className="font-semibold text-surface-900 dark:text-white truncate">{r.name}</h3>
                                <p className="text-sm text-surface-500 dark:text-gray-400">{r.email || r.phone}</p>
                                <div className="flex items-center gap-2 mt-2 flex-wrap">
                                    {r.flat_id && <span className="px-2 py-0.5 rounded-md text-xs bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 flex items-center gap-1"><Home className="w-3 h-3" />Flat #{r.flat_id}</span>}
                                    <span className={`px-2 py-0.5 rounded-md text-xs ${r.is_owner ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'}`}>
                                        {r.is_owner ? 'Owner' : 'Tenant'}
                                    </span>
                                    <span className={`px-2 py-0.5 rounded-md text-xs ${r.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                                        {r.is_active ? 'Active' : 'Inactive'}
                                    </span>
                                </div>
                            </div>
                            {r.flat_id && (
                                <button onClick={() => moveOut(r.id)} className="p-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-400 hover:text-red-500 transition-colors" title="Move out">
                                    <UserX className="w-4 h-4" />
                                </button>
                            )}
                        </div>
                    </motion.div>
                ))}
                {residents.length === 0 && <p className="text-center py-12 text-surface-400 col-span-full">No residents found</p>}
            </div>
        </div>
    );
}
