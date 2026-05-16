import sys

file_path = "d:\\ANTIGRAVITYFILESME\\GARAGEDOORSLEADS\\noahgaragedoors\\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "        <!-- BEFORE & AFTER -->"
end_marker = "        <!-- SERVICE AREAS -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found")
    sys.exit(1)

original_gallery_content = content[start_idx:end_idx]

inner_start = original_gallery_content.find("<!-- ─── DOOR INSTALLATIONS ─── -->")
inner_end = original_gallery_content.find("            </div>\n        </section>")
if inner_start == -1 or inner_end == -1:
    print("Inner markers not found")
    sys.exit(1)

full_items_html = original_gallery_content[inner_start:inner_end]

new_section = f"""        <!-- BEFORE & AFTER SHOWCASE -->
        <section id="gallery" class="py-20 px-4" style="background:#0a0a0a;">
            <div class="max-w-6xl mx-auto">
                <div class="text-center mb-16">
                    <div class="inline-flex items-center gap-2 glass-blue text-blue-400 text-xs font-black px-4 py-2 rounded-full mb-4 uppercase tracking-widest">
                        <i data-lucide="camera" class="w-3.5 h-3.5"></i> Real San Diego Jobs
                    </div>
                    <h2 class="text-3xl md:text-5xl font-black text-white mb-3">Before &amp; After</h2>
                    <p class="text-white/50 text-base max-w-xl mx-auto">Our most impressive recent jobs across San Diego County.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                    
                    <div class="glass rounded-2xl overflow-hidden hover:scale-[1.02] transition-transform">
                        <div class="grid grid-cols-2 h-64 md:h-80">
                            <div class="relative overflow-hidden">
                                <img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 left-3 text-xs font-black uppercase bg-red-600 text-white px-3 py-1 rounded-full shadow-lg">Before</span>
                            </div>
                            <div class="relative overflow-hidden border-l border-white/10">
                                <img src="gallery/AFTER17.jpeg" alt="New garage door with windows installed" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 right-3 text-xs font-black uppercase bg-green-600 text-white px-3 py-1 rounded-full shadow-lg">After</span>
                            </div>
                        </div>
                        <div class="px-6 py-4 border-t border-white/5">
                            <p class="text-lg font-bold text-white">Full Door Upgrade with Windows</p>
                            <p class="text-sm text-white/40">San Diego, CA</p>
                        </div>
                    </div>

                    <div class="glass rounded-2xl overflow-hidden hover:scale-[1.02] transition-transform">
                        <div class="grid grid-cols-2 h-64 md:h-80">
                            <div class="relative overflow-hidden">
                                <img src="gallery/BEFORE8.jpeg" alt="Old LiftMaster Formula2 opener" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 left-3 text-xs font-black uppercase bg-red-600 text-white px-3 py-1 rounded-full shadow-lg">Before</span>
                            </div>
                            <div class="relative overflow-hidden border-l border-white/10">
                                <img src="gallery/AFTER8.jpeg" alt="New Chamberlain myQ smart opener" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 right-3 text-xs font-black uppercase bg-green-600 text-white px-3 py-1 rounded-full shadow-lg">After</span>
                            </div>
                        </div>
                        <div class="px-6 py-4 border-t border-white/5">
                            <p class="text-lg font-bold text-white">Smart Opener Upgrade</p>
                            <p class="text-sm text-white/40">San Diego, CA</p>
                        </div>
                    </div>

                    <div class="glass rounded-2xl overflow-hidden hover:scale-[1.02] transition-transform">
                        <div class="grid grid-cols-2 h-64 md:h-80">
                            <div class="relative overflow-hidden">
                                <img src="gallery/BEFORE1.jpeg" alt="Old worn garage door springs" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 left-3 text-xs font-black uppercase bg-red-600 text-white px-3 py-1 rounded-full shadow-lg">Before</span>
                            </div>
                            <div class="relative overflow-hidden border-l border-white/10">
                                <img src="gallery/AFTER1.jpeg" alt="New garage door springs installed" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 right-3 text-xs font-black uppercase bg-green-600 text-white px-3 py-1 rounded-full shadow-lg">After</span>
                            </div>
                        </div>
                        <div class="px-6 py-4 border-t border-white/5">
                            <p class="text-lg font-bold text-white">Double Spring Replacement</p>
                            <p class="text-sm text-white/40">San Diego, CA</p>
                        </div>
                    </div>

                    <div class="glass rounded-2xl overflow-hidden hover:scale-[1.02] transition-transform">
                        <div class="grid grid-cols-2 h-64 md:h-80">
                            <div class="relative overflow-hidden">
                                <img src="gallery/BEFORE14.jpeg" alt="Old spring with orange tag on arched door" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 left-3 text-xs font-black uppercase bg-red-600 text-white px-3 py-1 rounded-full shadow-lg">Before</span>
                            </div>
                            <div class="relative overflow-hidden border-l border-white/10">
                                <img src="gallery/AFTER14.jpeg" alt="New spring on arched window garage door" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 right-3 text-xs font-black uppercase bg-green-600 text-white px-3 py-1 rounded-full shadow-lg">After</span>
                            </div>
                        </div>
                        <div class="px-6 py-4 border-t border-white/5">
                            <p class="text-lg font-bold text-white">Custom Door Spring Repair</p>
                            <p class="text-sm text-white/40">San Diego, CA</p>
                        </div>
                    </div>

                </div>

                <div class="text-center">
                    <button id="openGalleryBtn" class="inline-flex items-center justify-center gap-2 px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-full font-bold text-lg transition-all shadow-[0_0_20px_rgba(37,99,235,0.3)] hover:shadow-[0_0_30px_rgba(37,99,235,0.5)]">
                        View More Works <i data-lucide="images" class="w-5 h-5"></i>
                    </button>
                </div>
            </div>
        </section>

        <!-- FULL GALLERY MODAL -->
        <div id="fullGalleryModal" class="fixed inset-0 z-[100] w-screen h-screen backdrop-blur-xl bg-black/80 hidden flex-col items-center justify-start opacity-0 transition-opacity duration-300 overflow-hidden">
            <!-- Modal Content -->
            <div class="w-full h-full max-w-6xl mx-auto bg-[#0a0a0a] md:rounded-t-[2.5rem] md:mt-10 overflow-hidden flex flex-col relative border border-white/10 shadow-2xl transform translate-y-10 transition-transform duration-300" id="fullGalleryModalInner">
                <!-- Header -->
                <div class="flex justify-between items-center p-6 md:p-8 bg-black/40 border-b border-white/10 z-20">
                    <div>
                        <h2 class="text-2xl md:text-3xl font-black text-white">Full Job Gallery</h2>
                        <p class="text-white/50 text-sm mt-1">27+ real jobs completed across San Diego County.</p>
                    </div>
                    <button id="closeGalleryBtn" class="p-3 bg-white/10 hover:bg-white/20 text-white rounded-full transition-colors flex-shrink-0 border border-white/5">
                        <i data-lucide="x" class="w-6 h-6"></i>
                    </button>
                </div>
                <!-- Scrollable Body -->
                <div class="overflow-y-auto p-4 md:p-8 flex-1 custom-scrollbar">
{full_items_html}
                </div>
            </div>
        </div>
\n"""

new_content = content[:start_idx] + new_section + content[end_idx:]

js_to_add = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.getElementById('fullGalleryModal');
            const modalInner = document.getElementById('fullGalleryModalInner');
            const openBtn = document.getElementById('openGalleryBtn');
            const closeBtn = document.getElementById('closeGalleryBtn');

            function openModal() {
                modal.classList.remove('hidden');
                modal.classList.add('flex');
                // Trigger reflow
                void modal.offsetWidth;
                modal.classList.remove('opacity-0');
                modalInner.classList.remove('translate-y-10');
                document.body.style.overflow = 'hidden';
            }

            function closeModal() {
                modal.classList.add('opacity-0');
                modalInner.classList.add('translate-y-10');
                setTimeout(() => {
                    modal.classList.add('hidden');
                    modal.classList.remove('flex');
                    document.body.style.overflow = '';
                }, 300);
            }

            if (modal && openBtn && closeBtn) {
                openBtn.addEventListener('click', openModal);
                closeBtn.addEventListener('click', closeModal);

                // Close on click outside
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        closeModal();
                    }
                });
            }
        });
    </script>
"""

if "</body>" in new_content and "openGalleryBtn" not in content:
    new_content = new_content.replace("</body>", js_to_add + "</body>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully replaced gallery!")
