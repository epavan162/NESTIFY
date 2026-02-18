import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { Building2, Plus, Layers, DoorOpen } from 'lucide-react';

export default function SocietyPage() {
    const { user } = useAuth();
    const [societies, setSocieties] = useState<any[]>([]);
    const [towers, setTowers] = useState<any[]>([]);
    const [flats, setFlats] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedSociety, setSelectedSociety] = useState<number | null>(null);
    const [selectedTower, setSelectedTower] = useState<number | null>(null);
    const [showForm, setShowForm] = useState<string | null>(null);

    useEffect(() => { api.get('/societies/').then(r => { setSocieties(r.data); setLoading(false); if (r.data.length) setSelectedSociety(r.data[0].id); }).catch(() => setLoading(false)); }, []);
    useEffect(() => { if (selectedSociety) api.get(`/societies/${selectedSociety}/towers`).then(r => setTowers(r.data)); }, [selectedSociety]);
    useEffect(() => { if (selectedTower) api.get(`/societies/towers/${selectedTower}/flats`).then(r => setFlats(r.data)); }, [selectedTower]);

    const createSociety = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            const res = await api.post('/societies/', { name: fd.get('name'), address: fd.get('address'), city: fd.get('city'), state: fd.get('state'), pincode: fd.get('pincode') });
            toast.success('Society created');
            setSocieties([...societies, res.data]);
            setShowForm(null);
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const createTower = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            const res = await api.post('/societies/towers', { society_id: selectedSociety, name: fd.get('name'), total_floors: Number(fd.get('floors')) });
            toast.success('Tower added');
            setTowers([...towers, res.data]);
            setShowForm(null);
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const createFlat = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            const res = await api.post('/societies/flats', { tower_id: selectedTower, flat_number: fd.get('number'), floor: Number(fd.get('floor')), area_sqft: Number(fd.get('area')), flat_type: fd.get('type') });
            toast.success('Flat added');
            setFlats([...flats, res.data]);
            setShowForm(null);
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    if (loading) return <div className="space-y-3">{[1, 2, 3].map(i => <div key={i} className="skeleton h-20 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><Building2 className="w-6 h-6 text-primary-500" /> Society Management</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Manage societies, towers, and flats</p>
                </div>
                {user?.role === 'admin' && (
                    <div className="flex gap-2">
                        <button onClick={() => setShowForm('society')} className="btn-primary flex items-center gap-2 text-sm"><Plus className="w-4 h-4" />Society</button>
                        {selectedSociety && <button onClick={() => setShowForm('tower')} className="btn-secondary flex items-center gap-2 text-sm"><Plus className="w-4 h-4" />Tower</button>}
                        {selectedTower && <button onClick={() => setShowForm('flat')} className="btn-secondary flex items-center gap-2 text-sm"><Plus className="w-4 h-4" />Flat</button>}
                    </div>
                )}
            </div>

            {showForm === 'society' && (<motion.form onSubmit={createSociety} className="glass-card p-6 grid grid-cols-1 md:grid-cols-3 gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <input name="name" placeholder="Society Name" className="input-field" required />
                <input name="address" placeholder="Address" className="input-field" required />
                <input name="city" placeholder="City" className="input-field" required />
                <input name="state" placeholder="State" className="input-field" required />
                <input name="pincode" placeholder="Pincode" className="input-field" required />
                <button type="submit" className="btn-primary">Create</button>
            </motion.form>)}

            {showForm === 'tower' && (<motion.form onSubmit={createTower} className="glass-card p-6 grid grid-cols-1 md:grid-cols-3 gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <input name="name" placeholder="Tower Name" className="input-field" required />
                <input name="floors" type="number" placeholder="Total Floors" className="input-field" required />
                <button type="submit" className="btn-primary">Add Tower</button>
            </motion.form>)}

            {showForm === 'flat' && (<motion.form onSubmit={createFlat} className="glass-card p-6 grid grid-cols-1 md:grid-cols-4 gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <input name="number" placeholder="Flat Number" className="input-field" required />
                <input name="floor" type="number" placeholder="Floor" className="input-field" required />
                <input name="area" type="number" placeholder="Area (sqft)" className="input-field" />
                <select name="type" className="input-field"><option value="1BHK">1BHK</option><option value="2BHK">2BHK</option><option value="3BHK">3BHK</option><option value="4BHK">4BHK</option></select>
                <button type="submit" className="btn-primary">Add Flat</button>
            </motion.form>)}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Societies */}
                <div className="glass-card p-4">
                    <h3 className="font-semibold text-surface-800 dark:text-gray-200 mb-3 flex items-center gap-2"><Building2 className="w-4 h-4" />Societies</h3>
                    <div className="space-y-2">{societies.map(s => (
                        <button key={s.id} onClick={() => { setSelectedSociety(s.id); setSelectedTower(null); setFlats([]); }}
                            className={`w-full text-left p-3 rounded-xl transition-all ${selectedSociety === s.id ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800 border' : 'hover:bg-surface-50 dark:hover:bg-surface-800'}`}>
                            <p className="font-medium text-surface-900 dark:text-white">{s.name}</p>
                            <p className="text-xs text-surface-400">{s.city}, {s.state}</p>
                        </button>
                    ))}</div>
                </div>

                {/* Towers */}
                <div className="glass-card p-4">
                    <h3 className="font-semibold text-surface-800 dark:text-gray-200 mb-3 flex items-center gap-2"><Layers className="w-4 h-4" />Towers</h3>
                    <div className="space-y-2">{towers.map(t => (
                        <button key={t.id} onClick={() => setSelectedTower(t.id)}
                            className={`w-full text-left p-3 rounded-xl transition-all ${selectedTower === t.id ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800 border' : 'hover:bg-surface-50 dark:hover:bg-surface-800'}`}>
                            <p className="font-medium text-surface-900 dark:text-white">{t.name}</p>
                            <p className="text-xs text-surface-400">{t.total_floors} floors</p>
                        </button>
                    ))}</div>
                    {towers.length === 0 && <p className="text-sm text-surface-400 text-center py-4">Select a society</p>}
                </div>

                {/* Flats */}
                <div className="glass-card p-4">
                    <h3 className="font-semibold text-surface-800 dark:text-gray-200 mb-3 flex items-center gap-2"><DoorOpen className="w-4 h-4" />Flats</h3>
                    <div className="space-y-2">{flats.map(f => (
                        <div key={f.id} className="p-3 rounded-xl bg-surface-50 dark:bg-surface-800">
                            <p className="font-medium text-surface-900 dark:text-white">{f.flat_number}</p>
                            <p className="text-xs text-surface-400">Floor {f.floor} • {f.flat_type} • {f.area_sqft} sqft</p>
                        </div>
                    ))}</div>
                    {flats.length === 0 && <p className="text-sm text-surface-400 text-center py-4">Select a tower</p>}
                </div>
            </div>
        </div>
    );
}
