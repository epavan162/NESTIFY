import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { Vote, Plus, BarChart3, CheckCircle2 } from 'lucide-react';

export default function PollsPage() {
    const { user } = useAuth();
    const [polls, setPolls] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showCreate, setShowCreate] = useState(false);
    const [newOptions, setNewOptions] = useState(['', '']);

    useEffect(() => { fetchPolls(); }, []);
    const fetchPolls = () => { api.get('/polls/').then(r => { setPolls(r.data); setLoading(false); }).catch(() => setLoading(false)); };

    const createPoll = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const fd = new FormData(e.currentTarget);
        const opts = newOptions.filter(o => o.trim());
        if (opts.length < 2) { toast.error('Need at least 2 options'); return; }
        try {
            await api.post('/polls/', { question: fd.get('question'), options: opts });
            toast.success('Poll created');
            setShowCreate(false);
            setNewOptions(['', '']);
            fetchPolls();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Failed'); }
    };

    const castVote = async (pollId: number, optionIndex: number) => {
        try {
            await api.post(`/polls/${pollId}/vote`, { option_index: optionIndex });
            toast.success('Vote recorded');
            fetchPolls();
        } catch (err: any) { toast.error(err.response?.data?.detail || 'Already voted'); }
    };

    if (loading) return <div className="space-y-3">{[1, 2].map(i => <div key={i} className="skeleton h-40 rounded-xl" />)}</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-surface-900 dark:text-white flex items-center gap-2"><Vote className="w-6 h-6 text-primary-500" /> Polls & Voting</h2>
                    <p className="text-surface-500 dark:text-gray-400 text-sm">Community decisions</p>
                </div>
                {user?.role === 'admin' && <button onClick={() => setShowCreate(!showCreate)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />Create Poll</button>}
            </div>

            {showCreate && (
                <motion.form onSubmit={createPoll} className="glass-card p-6 space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <input name="question" placeholder="Poll Question" className="input-field" required />
                    {newOptions.map((opt, idx) => (
                        <input key={idx} value={opt} onChange={(e) => { const n = [...newOptions]; n[idx] = e.target.value; setNewOptions(n); }}
                            placeholder={`Option ${idx + 1}`} className="input-field" required={idx < 2} />
                    ))}
                    <button type="button" onClick={() => setNewOptions([...newOptions, ''])} className="btn-secondary text-sm">+ Add Option</button>
                    <button type="submit" className="btn-primary w-full">Create Poll</button>
                </motion.form>
            )}

            <div className="space-y-6">
                {polls.map((poll, pi) => {
                    const totalVotes = poll.total_votes || 0;
                    return (
                        <motion.div key={poll.id} className="glass-card p-6" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: pi * 0.1 }}>
                            <h3 className="text-lg font-semibold text-surface-900 dark:text-white mb-1">{poll.question}</h3>
                            <p className="text-sm text-surface-400 mb-4 flex items-center gap-1"><BarChart3 className="w-3.5 h-3.5" />{totalVotes} votes</p>
                            <div className="space-y-3">
                                {poll.options.map((opt: string, idx: number) => {
                                    const count = poll.vote_counts?.[idx] || 0;
                                    const pct = totalVotes > 0 ? Math.round((count / totalVotes) * 100) : 0;
                                    const isVoted = poll.user_voted === idx;
                                    return (
                                        <button key={idx} onClick={() => castVote(poll.id, idx)} disabled={poll.user_voted !== null && poll.user_voted !== undefined}
                                            className={`w-full text-left relative overflow-hidden rounded-xl p-3 border transition-all ${isVoted ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : 'border-surface-200 dark:border-surface-700 hover:border-primary-300'}`}>
                                            <div className="absolute inset-0 bg-primary-500/10 dark:bg-primary-500/20 rounded-xl" style={{ width: `${pct}%` }} />
                                            <div className="relative flex items-center justify-between">
                                                <span className="font-medium text-surface-800 dark:text-gray-200 flex items-center gap-2">
                                                    {isVoted && <CheckCircle2 className="w-4 h-4 text-primary-500" />}{opt}
                                                </span>
                                                <span className="text-sm font-semibold text-surface-600 dark:text-gray-400">{pct}% ({count})</span>
                                            </div>
                                        </button>
                                    );
                                })}
                            </div>
                        </motion.div>
                    );
                })}
                {polls.length === 0 && <p className="text-center py-12 text-surface-400">No active polls</p>}
            </div>
        </div>
    );
}
