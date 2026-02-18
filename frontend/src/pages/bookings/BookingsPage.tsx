import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import api from '@/api/client';
import { toast } from 'sonner';
import { CalendarDays, Plus, Clock, XCircle } from 'lucide-react';

const FACILITIES = ['Gym', 'Party Hall', 'Swimming Pool', 'Clubhouse', 'Tennis Court'];

export default function BookingsPage() {
    const [bookings, setBookings] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showCreate, setShowCreate] = useState(false);

    useEffect(() => { fetchBookings(); }, []);
    const fetchBookings = () => { api.get('/bookings/').then(r => { setBookings(r.data); setLoading(false); }).catch(() => setLoading(false)); };

    const createBooking = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            await api.post('/bookings/', {
                facility_name: fd.get('facility'), booking_date: fd.get('date'), start_time: fd.get('start'), end_time: fd.get('end'),
            });
            toast.success('Booking confirmed!');
            setShowCreate(false);
            fetchBookings();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Booking failed'); }
    };

    const cancelBooking = async (id: number) => {
        try { await api.delete(`/bookings/${id}`); toast.success('Booking cancelled'); fetchBookings(); } catch { toast.error('Failed'); }
    };

    if (loading) return <div className="space-y-3">{[1, 2, 3].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><CalendarDays className="w-6 h-6 text-primary-500" /> Facility Booking</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Book amenities and facilities</p>
                </div>
                <button onClick={() => setShowCreate(!showCreate)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />Book Now</button>
            </div>

            {showCreate && (
                <motion.form onSubmit={createBooking} className="glass-card p-6 grid grid-cols-1 md:grid-cols-2 gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <select name="facility" className="input-field" required>
                        <option value="">Select Facility</option>
                        {FACILITIES.map(f => <option key={f} value={f}>{f}</option>)}
                    </select>
                    <input name="date" type="date" className="input-field" required />
                    <input name="start" type="time" className="input-field" required />
                    <input name="end" type="time" className="input-field" required />
                    <button type="submit" className="btn-primary md:col-span-2">Confirm Booking</button>
                </motion.form>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {bookings.map((b, i) => (
                    <motion.div key={b.id} className="glass-card p-5" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.05 }}>
                        <div className="flex items-start justify-between">
                            <div>
                                <h3 className="font-semibold text-surface-900 dark:text-white">{b.facility_name}</h3>
                                <p className="text-sm text-surface-500 dark:text-gray-400 flex items-center gap-1 mt-1"><CalendarDays className="w-3.5 h-3.5" />{b.booking_date}</p>
                                <p className="text-sm text-surface-500 dark:text-gray-400 flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{b.start_time} – {b.end_time}</p>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`px-3 py-1 rounded-full text-xs font-medium ${b.status === 'confirmed' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' : 'bg-red-100 text-red-700'}`}>{b.status}</span>
                                {b.status === 'confirmed' && (
                                    <button onClick={() => cancelBooking(b.id)} className="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-500"><XCircle className="w-4 h-4" /></button>
                                )}
                            </div>
                        </div>
                    </motion.div>
                ))}
                {bookings.length === 0 && <p className="text-center py-12 text-surface-400 md:col-span-2">No bookings yet</p>}
            </div>
        </div>
    );
}
