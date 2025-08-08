'use client'

import React, { useState, useEffect, useRef } from 'react';
import { Search, Home, MessageSquare, Mail, User, FileText, CheckCircle, Settings, Music, Rocket, Sparkles, X, Menu, Bell, Plus, Heart, MessageCircle, Send, Bookmark, MoreHorizontal, Globe, Code, Palette } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SuperNovaApp() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentUniverse, setCurrentUniverse] = useState('feed');
  const [searchFocused, setSearchFocused] = useState(false);
  const [likedPosts, setLikedPosts] = useState(new Set());
  const [bookmarkedPosts, setBookmarkedPosts] = useState(new Set());
  const sidebarRef = useRef(null);

  // Close sidebar when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (sidebarRef.current && !sidebarRef.current.contains(event.target)) {
        setSidebarOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const universes = [
    { id: 'feed', label: 'Feed', icon: Home, color: 'from-purple-500 to-pink-500' },
    { id: 'chat', label: 'Chat', icon: MessageSquare, color: 'from-blue-500 to-cyan-500' },
    { id: 'messages', label: 'Messages', icon: Mail, color: 'from-green-500 to-emerald-500' },
    { id: 'profile', label: 'Profile', icon: User, color: 'from-orange-500 to-red-500' },
    { id: 'proposals', label: 'Proposals', icon: FileText, color: 'from-indigo-500 to-purple-500' },
    { id: 'decisions', label: 'Decisions', icon: CheckCircle, color: 'from-teal-500 to-green-500' },
    { id: 'execution', label: 'Execution', icon: Settings, color: 'from-gray-500 to-gray-700' },
    { id: 'metaverse', label: 'Enter Metaverse', icon: Globe, color: 'from-pink-500 to-rose-500' },
    { id: 'universe2d', label: 'Universe2D', icon: Palette, color: 'from-yellow-500 to-orange-500' },
    { id: 'page-ai', label: 'Page AI', icon: Code, color: 'from-cyan-500 to-blue-500' },
  ];

  const posts = [
    {
      id: 1,
      author: 'taha_gungor',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=taha',
      content: 'Just launched superNova_2177 🚀 Mathematically sucked into a void of innovation!',
      likes: 342,
      comments: 28,
      time: '2h ago',
      image: 'https://picsum.photos/600/400?random=1',
      universe: 'feed'
    },
    {
      id: 2,
      author: 'test_tech',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=tech',
      content: 'New proposal: Implement weighted voting system for AI entities 🤖',
      likes: 156,
      comments: 42,
      time: '5h ago',
      universe: 'proposals'
    },
    {
      id: 3,
      author: 'globalrunway',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=global',
      content: 'The future of decentralized decision-making is here. Join us in the metaverse! ✨',
      likes: 892,
      comments: 103,
      time: '1d ago',
      image: 'https://picsum.photos/600/600?random=2',
      universe: 'metaverse'
    },
  ];

  const stories = [
    { id: 1, name: 'Your Story', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=you', isUser: true },
    { id: 2, name: 'test_tech', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=tech' },
    { id: 3, name: 'nova_ai', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=ai' },
    { id: 4, name: 'metaverse', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=meta' },
    { id: 5, name: 'global', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=global' },
  ];

  const handleLike = (postId) => {
    setLikedPosts(prev => {
      const newSet = new Set(prev);
      if (newSet.has(postId)) {
        newSet.delete(postId);
      } else {
        newSet.add(postId);
      }
      return newSet;
    });
  };

  const handleBookmark = (postId) => {
    setBookmarkedPosts(prev => {
      const newSet = new Set(prev);
      if (newSet.has(postId)) {
        newSet.delete(postId);
      } else {
        newSet.add(postId);
      }
      return newSet;
    });
  };

  const renderUniverse = () => {
    const universe = universes.find(u => u.id === currentUniverse);
    
    return (
      <motion.div
        key={currentUniverse}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
        className="min-h-screen"
      >
        {/* Universe Header */}
        <div className={`bg-gradient-to-r ${universe?.color || 'from-purple-500 to-pink-500'} p-8 rounded-2xl mb-8`}>
          <h2 className="text-4xl font-bold mb-2">{universe?.label} Universe</h2>
          <p className="text-white/80">Explore the {universe?.label?.toLowerCase()} dimension of superNova_2177</p>
        </div>

        {/* Stories - Only show in feed universe */}
        {currentUniverse === 'feed' && (
          <div className="flex space-x-4 overflow-x-auto pb-4 mb-8">
            {stories.map((story) => (
              <motion.button
                key={story.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex-shrink-0 text-center"
              >
                <div className={`w-16 h-16 rounded-full p-0.5 ${story.isUser ? 'bg-gray-700' : 'bg-gradient-to-tr from-purple-500 to-pink-500'}`}>
                  <div className="w-full h-full rounded-full bg-black p-0.5">
                    <img
                      src={story.avatar}
                      alt={story.name}
                      className="w-full h-full rounded-full"
                    />
                  </div>
                </div>
                <p className="text-xs mt-1">{story.name}</p>
              </motion.button>
            ))}
          </div>
        )}

        {/* Universe-specific content */}
        {currentUniverse === 'metaverse' && (
          <div className="mb-8 p-6 bg-gradient-to-r from-purple-900/20 to-pink-900/20 rounded-xl border border-purple-500/30">
            <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
              🌌 Metaverse Portal Active
            </h3>
            <p className="text-gray-300 mb-4">
              You're now connected to the superNova metaverse. Experience decentralized reality.
            </p>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-black/40 p-4 rounded-lg text-center">
                <div className="text-3xl mb-2">🌍</div>
                <p className="text-sm">World 1</p>
              </div>
              <div className="bg-black/40 p-4 rounded-lg text-center">
                <div className="text-3xl mb-2">🌎</div>
                <p className="text-sm">World 2</p>
              </div>
              <div className="bg-black/40 p-4 rounded-lg text-center">
                <div className="text-3xl mb-2">🌏</div>
                <p className="text-sm">World 3</p>
              </div>
            </div>
          </div>
        )}

        {currentUniverse === 'universe2d' && (
          <div className="mb-8 p-6 bg-gradient-to-r from-yellow-900/20 to-orange-900/20 rounded-xl border border-yellow-500/30">
            <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-400">
              🎨 Universe2D Canvas
            </h3>
            <div className="aspect-video bg-black/40 rounded-lg flex items-center justify-center">
              <p className="text-gray-400">2D Universe Rendering Engine</p>
            </div>
          </div>
        )}

        {currentUniverse === 'page-ai' && (
          <div className="mb-8 p-6 bg-gradient-to-r from-cyan-900/20 to-blue-900/20 rounded-xl border border-cyan-500/30">
            <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
              🤖 AI Page Generator
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Describe your universe..."
                className="w-full p-3 bg-black/40 rounded-lg border border-cyan-500/30 focus:border-cyan-400 outline-none"
              />
              <button className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-semibold hover:opacity-90 transition-opacity">
                Generate Universe
              </button>
            </div>
          </div>
        )}

        {/* Posts */}
        <div className="space-y-6">
          {posts.filter(post => currentUniverse === 'feed' || post.universe === currentUniverse).map((post) => (
            <motion.article
              key={post.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              whileHover={{ scale: 1.01 }}
              className="bg-gray-950 border border-gray-800 rounded-xl overflow-hidden"
            >
              {/* Post Header */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center space-x-3">
                  <img
                    src={post.avatar}
                    alt={post.author}
                    className="w-10 h-10 rounded-full"
                  />
                  <div>
                    <p className="font-semibold">{post.author}</p>
                    <p className="text-xs text-gray-400">{post.time}</p>
                  </div>
                </div>
                <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                  <MoreHorizontal className="w-5 h-5" />
                </button>
              </div>

              {/* Post Content */}
              <div className="px-4 pb-3">
                <p className="text-sm">{post.content}</p>
              </div>

              {/* Post Image */}
              {post.image && (
                <img
                  src={post.image}
                  alt="Post"
                  className="w-full"
                />
              )}

              {/* Actions */}
              <div className="flex items-center justify-between p-4 border-t border-gray-800">
                <div className="flex items-center space-x-4">
                  <motion.button
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleLike(post.id)}
                    className={`flex items-center space-x-2 transition-colors ${
                      likedPosts.has(post.id) ? 'text-red-500' : 'hover:text-red-500'
                    }`}
                  >
                    <Heart className={`w-5 h-5 ${likedPosts.has(post.id) ? 'fill-current' : ''}`} />
                    <span className="text-sm">{likedPosts.has(post.id) ? post.likes + 1 : post.likes}</span>
                  </motion.button>
                  <button className="flex items-center space-x-2 hover:text-blue-500 transition-colors">
                    <MessageCircle className="w-5 h-5" />
                    <span className="text-sm">{post.comments}</span>
                  </button>
                  <button className="hover:text-purple-500 transition-colors">
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                <motion.button
                  whileTap={{ scale: 0.9 }}
                  onClick={() => handleBookmark(post.id)}
                  className={`transition-colors ${
                    bookmarkedPosts.has(post.id) ? 'text-yellow-500' : 'hover:text-yellow-500'
                  }`}
                >
                  <Bookmark className={`w-5 h-5 ${bookmarkedPosts.has(post.id) ? 'fill-current' : ''}`} />
                </motion.button>
              </div>
            </motion.article>
          ))}
        </div>
      </motion.div>
    );
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Top Navigation Bar */}
      <nav className="fixed top-0 left-0 right-0 bg-gray-950/80 backdrop-blur-xl border-b border-gray-800 z-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                superNova_2177
              </h1>
            </div>

            {/* Search Bar */}
            <div className={`hidden md:flex items-center bg-gray-900 rounded-xl px-4 py-2 transition-all duration-200 ${searchFocused ? 'w-96 ring-2 ring-purple-500' : 'w-64'}`}>
              <Search className="w-4 h-4 text-gray-400 mr-2" />
              <input
                type="text"
                placeholder="Search universes..."
                className="bg-transparent outline-none text-sm flex-1 placeholder-gray-500"
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
              />
            </div>

            {/* Right Actions */}
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                <Home className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                <MessageSquare className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                <Plus className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors relative">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
              </button>
              
              {/* Profile Picture - Triggers Sidebar */}
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="w-8 h-8 rounded-full overflow-hidden ring-2 ring-purple-500 hover:ring-purple-400 transition-all"
              >
                <img
                  src="https://api.dicebear.com/7.x/avataaars/svg?seed=taha"
                  alt="Profile"
                  className="w-full h-full"
                />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Sidebar Overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          />
        )}
      </AnimatePresence>

      {/* Sliding Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            ref={sidebarRef}
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed top-0 right-0 h-full w-80 bg-gray-950 border-l border-gray-800 z-50 overflow-y-auto"
          >
            <div className="p-6">
              {/* Close Button */}
              <button
                onClick={() => setSidebarOpen(false)}
                className="absolute top-4 right-4 p-2 hover:bg-gray-800 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              {/* Profile Section */}
              <div className="mb-8">
                <div className="flex items-center space-x-4 mb-6">
                  <img
                    src="https://api.dicebear.com/7.x/avataaars/svg?seed=taha"
                    alt="Profile"
                    className="w-16 h-16 rounded-full ring-2 ring-purple-500"
                  />
                  <div>
                    <h3 className="font-bold text-lg">taha_gungor</h3>
                    <p className="text-gray-400 text-sm">CEO / test_tech</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 p-4 bg-gray-900 rounded-xl">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-purple-400">2.4K</p>
                    <p className="text-xs text-gray-400">Profile Views</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-pink-400">1.6K</p>
                    <p className="text-xs text-gray-400">Impressions</p>
                  </div>
                </div>
              </div>

              {/* Universe Navigation */}
              <div className="space-y-1 mb-6">
                <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Universes</p>
                {universes.map((universe) => (
                  <motion.button
                    key={universe.id}
                    whileHover={{ x: 4 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => {
                      setCurrentUniverse(universe.id);
                      setSidebarOpen(false);
                    }}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                      currentUniverse === universe.id
                        ? 'bg-purple-500/20 text-purple-400'
                        : 'hover:bg-gray-800 text-gray-300'
                    }`}
                  >
                    <universe.icon className="w-5 h-5" />
                    <span className="font-medium">{universe.label}</span>
                  </motion.button>
                ))}
              </div>

              {/* Premium Section */}
              <div className="space-y-1 mb-6">
                <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Premium</p>
                <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-800 text-gray-300 transition-all">
                  <Music className="w-5 h-5" />
                  <span className="font-medium">Music</span>
                </button>
                <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-800 text-gray-300 transition-all">
                  <Rocket className="w-5 h-5" />
                  <span className="font-medium">Agents</span>
                </button>
              </div>

              {/* Settings */}
              <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-800 text-gray-300 transition-all">
                <Settings className="w-5 h-5" />
                <span className="font-medium">Settings</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 pt-24 pb-20">
        <AnimatePresence mode="wait">
          {renderUniverse()}
        </AnimatePresence>
      </main>
    </div>
  );
}

