import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { Receipt, Plus, CheckCircle, Clock, AlertTriangle, CreditCard } from 'lucide-react';

export default function MaintenancePage() {
    const { user } = useAuth();
    const [invoices, setInvoices] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showCreate, setShowCreate] = useState(false);

    useEffect(() => { fetchInvoices(); }, []);

    const fetchInvoices = () => {
        api.get('/maintenance/invoices').then(r => { setInvoices(r.data); setLoading(false); }).catch(() => setLoading(false));
    };

    const createInvoice = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        try {
            await api.post('/maintenance/invoices', {
                flat_id: Number(fd.get('flat_id')), amount: Number(fd.get('amount')),
                due_date: fd.get('due_date'), month: Number(fd.get('month')), year: Number(fd.get('year')),
            });
            toast.success('Invoice created');
            setShowCreate(false);
            fetchInvoices();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const makePayment = async (invoice: any) => {
        try {
            await api.post('/maintenance/payments', { invoice_id: invoice.id, amount: invoice.total_amount, payment_method: 'upi' });
            toast.success('Payment recorded');
            fetchInvoices();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const statusIcon = (s: string) => s === 'paid' ? <CheckCircle className="w-4 h-4 text-green-500" /> : s === 'overdue' ? <AlertTriangle className="w-4 h-4 text-red-500" /> : <Clock className="w-4 h-4 text-amber-500" />;
    const statusColor = (s: string) => s === 'paid' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' : s === 'overdue' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300';

    if (loading) return <div className="space-y-3">{[1, 2, 3, 4].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><Receipt className="w-6 h-6 text-primary-500" /> Maintenance Billing</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Manage invoices and payments</p>
                </div>
                {['admin', 'treasurer'].includes(user?.role || '') && (
                    <button onClick={() => setShowCreate(!showCreate)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />Create Invoice</button>
                )}
            </div>

            {showCreate && (
                <motion.form onSubmit={createInvoice} className="glass-card p-6 grid grid-cols-1 md:grid-cols-3 gap-4" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}>
                    <input name="flat_id" type="number" placeholder="Flat ID" className="input-field" required />
                    <input name="amount" type="number" step="0.01" placeholder="Amount (₹)" className="input-field" required />
                    <input name="due_date" type="date" className="input-field" required />
                    <input name="month" type="number" placeholder="Month (1-12)" min="1" max="12" className="input-field" required />
                    <input name="year" type="number" placeholder="Year" className="input-field" required />
                    <button type="submit" className="btn-primary">Create</button>
                </motion.form>
            )}

            <div className="space-y-3">
                {invoices.map((inv, i) => (
                    <motion.div key={inv.id} className="glass-card p-4 flex items-center justify-between hover:shadow-card-hover transition-all" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}>
                        <div className="flex items-center gap-4">
                            <div className="p-2.5 rounded-xl bg-primary-100 dark:bg-primary-900/30">
                                <Receipt className="w-5 h-5 text-primary-600 dark:text-primary-400" />
                            </div>
                            <div>
                                <p className="font-medium text-surface-900 dark:text-white">Flat #{inv.flat_id} — {inv.month}/{inv.year}</p>
                                <p className="text-sm text-surface-500">Due: {inv.due_date} {inv.late_fee > 0 && `| Late Fee: ₹${inv.late_fee}`}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <p className="text-lg font-bold text-surface-900 dark:text-white">₹{inv.total_amount.toLocaleString()}</p>
                            <span className={`px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${statusColor(inv.status)}`}>
                                {statusIcon(inv.status)} {inv.status}
                            </span>
                            {inv.status !== 'paid' && (
                                <button onClick={() => makePayment(inv)} className="btn-primary text-sm px-4 py-1.5 flex items-center gap-1">
                                    <CreditCard className="w-3.5 h-3.5" /> Pay
                                </button>
                            )}
                        </div>
                    </motion.div>
                ))}
                {invoices.length === 0 && <p className="text-center py-12 text-surface-400">No invoices found</p>}
            </div>
        </div>
    );
}
