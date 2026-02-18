import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '@/store/AuthContext';
import { useTheme } from '@/store/ThemeContext';
import api from '@/api/client';
import { toast } from 'sonner';
import { Home, Mail, Phone, ArrowRight, Sun, Moon, Loader2 } from 'lucide-react';

export default function LoginPage() {
    const { login } = useAuth();
    const { isDark, toggle } = useTheme();
    const navigate = useNavigate();
    const [tab, setTab] = useState<'email' | 'phone'>('email');
    const [loading, setLoading] = useState(false);

    // Email login
    const [email, setEmail] = useState('admin@nestify.com');
    const [password, setPassword] = useState('admin123');

    // Phone OTP
    const [phone, setPhone] = useState('');
    const [otpSent, setOtpSent] = useState(false);
    const [otp, setOtp] = useState('');
    const [name, setName] = useState('');

    const handleEmailLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.post('/auth/login', { email, password });
            login(res.data.access_token, res.data.user);
            toast.success('Welcome back!');
            navigate('/dashboard');
        } catch (err: any) {
            toast.error(err.response?.data?.detail || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    const sendOTP = async () => {
        setLoading(true);
        try {
            const res = await api.post('/auth/otp/send', { phone });
            toast.success(`OTP sent! (Dev: ${res.data.otp_dev})`);
            setOtpSent(true);
        } catch (err: any) {
            toast.error('Failed to send OTP');
        } finally {
            setLoading(false);
        }
    };

    const verifyOTP = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.post('/auth/otp/verify', { phone, otp, name: name || undefined });
            login(res.data.access_token, res.data.user);
            toast.success('Welcome!');
            navigate('/dashboard');
        } catch (err: any) {
            toast.error(err.response?.data?.detail || 'OTP verification failed');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = async () => {
        try {
            const res = await api.get('/auth/google/url');
            window.location.href = res.data.url;
        } catch {
            toast.error('Google login unavailable');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
            {/* Animated Background */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary-500/20 via-transparent to-accent-500/20 dark:from-primary-900/40 dark:via-[#0f1019] dark:to-accent-900/30" />
            <div className="absolute top-0 left-0 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-accent-500/20 rounded-full blur-3xl animate-pulse delay-1000" />

            {/* Theme Toggle */}
            <button onClick={toggle} className="absolute top-6 right-6 p-2.5 rounded-xl glass-card hover:scale-105 transition-transform z-10">
                {isDark ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-primary-600" />}
            </button>

            {/* Login Card */}
            <motion.div
                className="relative z-10 w-full max-w-md mx-4"
                initial={{ opacity: 0, y: 30, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
            >
                <div className="glass-card p-8 space-y-6">
                    {/* Logo */}
                    <div className="text-center space-y-2">
                        <motion.div
                            className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-xl shadow-primary-500/30"
                            whileHover={{ rotate: 5 }}
                        >
                            <Home className="w-8 h-8 text-white" />
                        </motion.div>
                        <h1 className="text-3xl font-bold gradient-text">Nestify</h1>
                        <p className="text-surface-500 dark:text-gray-400">Premium Apartment Management</p>
                    </div>

                    {/* Tabs */}
                    <div className="flex bg-surface-100 dark:bg-surface-800 rounded-xl p-1">
                        <button
                            onClick={() => { setTab('email'); setOtpSent(false); }}
                            className={`flex-1 py-2.5 rounded-lg text-sm font-medium transition-all ${tab === 'email' ? 'bg-white dark:bg-surface-700 shadow-sm text-primary-600' : 'text-surface-500'}`}
                        >
                            <Mail className="w-4 h-4 inline mr-2" />Email
                        </button>
                        <button
                            onClick={() => setTab('phone')}
                            className={`flex-1 py-2.5 rounded-lg text-sm font-medium transition-all ${tab === 'phone' ? 'bg-white dark:bg-surface-700 shadow-sm text-primary-600' : 'text-surface-500'}`}
                        >
                            <Phone className="w-4 h-4 inline mr-2" />Phone
                        </button>
                    </div>

                    {/* Email Login Form */}
                    {tab === 'email' && (
                        <motion.form onSubmit={handleEmailLogin} className="space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                            <div>
                                <label className="block text-sm font-medium text-surface-600 dark:text-gray-300 mb-1.5">Email</label>
                                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="input-field" placeholder="admin@nestify.com" required />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-surface-600 dark:text-gray-300 mb-1.5">Password</label>
                                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="input-field" placeholder="••••••••" required />
                            </div>
                            <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2">
                                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Sign In <ArrowRight className="w-4 h-4" /></>}
                            </button>
                        </motion.form>
                    )}

                    {/* Phone OTP Form */}
                    {tab === 'phone' && (
                        <motion.div className="space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                            {!otpSent ? (
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-surface-600 dark:text-gray-300 mb-1.5">Phone Number</label>
                                        <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} className="input-field" placeholder="9876543210" required />
                                    </div>
                                    <button onClick={sendOTP} disabled={loading || !phone} className="btn-primary w-full flex items-center justify-center gap-2">
                                        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Send OTP <ArrowRight className="w-4 h-4" /></>}
                                    </button>
                                </div>
                            ) : (
                                <form onSubmit={verifyOTP} className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-surface-600 dark:text-gray-300 mb-1.5">Your Name</label>
                                        <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="input-field" placeholder="John Doe" />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-surface-600 dark:text-gray-300 mb-1.5">Enter OTP</label>
                                        <input type="text" value={otp} onChange={(e) => setOtp(e.target.value)} className="input-field text-center text-2xl tracking-[0.5em]" placeholder="000000" maxLength={6} required />
                                    </div>
                                    <button type="submit" disabled={loading || otp.length < 6} className="btn-primary w-full flex items-center justify-center gap-2">
                                        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Verify & Login <ArrowRight className="w-4 h-4" /></>}
                                    </button>
                                    <button type="button" onClick={() => setOtpSent(false)} className="btn-secondary w-full text-sm">
                                        Change Number
                                    </button>
                                </form>
                            )}
                        </motion.div>
                    )}

                    {/* Divider */}
                    <div className="flex items-center gap-3">
                        <div className="flex-1 h-px bg-surface-200 dark:bg-surface-700" />
                        <span className="text-xs text-surface-400">OR</span>
                        <div className="flex-1 h-px bg-surface-200 dark:bg-surface-700" />
                    </div>

                    {/* Google OAuth */}
                    <button onClick={handleGoogleLogin} className="btn-secondary w-full flex items-center justify-center gap-3">
                        <svg className="w-5 h-5" viewBox="0 0 24 24">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                        </svg>
                        Continue with Google
                    </button>

                    {/* Demo Credentials */}
                    <div className="text-center text-xs text-surface-400 dark:text-gray-500 space-y-1">
                        <p className="font-medium">Demo Credentials:</p>
                        <p>Admin: admin@nestify.com / admin123</p>
                        <p>Resident: priya@nestify.com / resident123</p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
