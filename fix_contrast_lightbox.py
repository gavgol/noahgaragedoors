import sys

file_path = "d:\\ANTIGRAVITYFILESME\\GARAGEDOORSLEADS\\noahgaragedoors\\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update hero gradient for better contrast
old_gradient = "background: linear-gradient(to bottom, rgba(10, 10, 15, 0.3), rgba(10, 10, 15, 0.95));"
new_gradient = "background: linear-gradient(to bottom, rgba(10, 10, 15, 0.65), rgba(10, 10, 15, 0.95));"
content = content.replace(old_gradient, new_gradient)

# 2. Add text shadow to Hero Text
old_h1 = '<h1 class="text-4xl md:text-7xl font-black leading-[1.05] mb-5 text-white animate-blur-up delay-100">'
new_h1 = '<h1 class="text-4xl md:text-7xl font-black leading-[1.05] mb-5 text-white animate-blur-up delay-100" style="text-shadow: 0 4px 24px rgba(0,0,0,0.8);">'
content = content.replace(old_h1, new_h1)

old_p = '<p class="text-lg md:text-xl text-white/70 font-light max-w-2xl mb-8 animate-blur-up delay-200">'
new_p = '<p class="text-lg md:text-xl text-white/90 font-light max-w-2xl mb-8 animate-blur-up delay-200" style="text-shadow: 0 2px 10px rgba(0,0,0,0.8);">'
content = content.replace(old_p, new_p)


# 3. Replace the old Lightbox Modal HTML with a foolproof version
old_lightbox_html = """        <!-- LIGHTBOX MODAL -->
        <div id="lightboxModal" class="fixed inset-0 z-[200] w-screen h-screen bg-black/95 hidden flex-col items-center justify-center opacity-0 transition-opacity duration-300">
            <button id="closeLightboxBtn" class="absolute top-6 right-6 p-3 bg-white/10 hover:bg-white/20 text-white rounded-full transition-colors z-[210]">
                <i data-lucide="x" class="w-6 h-6"></i>
            </button>
            <div class="w-full h-full p-4 flex items-center justify-center">
                <img id="lightboxImg" src="" alt="Enlarged view" class="max-w-full max-h-full object-contain transform scale-95 transition-transform duration-300">
            </div>
        </div>"""

new_lightbox_html = """        <!-- LIGHTBOX MODAL -->
        <div id="lightboxModal" style="z-index: 99999; background-color: rgba(0,0,0,0.95);" class="fixed inset-0 w-screen h-screen hidden flex-col items-center justify-center opacity-0 transition-opacity duration-300">
            <button id="closeLightboxBtn" onclick="closeLightbox()" style="z-index: 100000;" class="absolute top-6 right-6 p-4 bg-white/20 hover:bg-white/30 text-white rounded-full transition-colors cursor-pointer">
                <i data-lucide="x" class="w-8 h-8"></i>
            </button>
            <div class="w-full h-full p-4 flex items-center justify-center" onclick="closeLightbox()" style="cursor: zoom-out;">
                <img id="lightboxImg" src="" alt="Enlarged view" class="max-w-full max-h-full object-contain transform scale-95 transition-transform duration-300" onclick="event.stopPropagation();" style="cursor: default;">
            </div>
        </div>"""
content = content.replace(old_lightbox_html, new_lightbox_html)

# 4. Pull the Lightbox JS out of DOMContentLoaded to make it 100% available globally immediately
old_js = """
            // Global Lightbox logic
            window.openLightbox = function(src) {
                const lightboxModal = document.getElementById('lightboxModal');
                const lightboxImg = document.getElementById('lightboxImg');
                if (!lightboxModal || !lightboxImg) return;
                
                lightboxImg.src = src;
                lightboxModal.classList.remove('hidden');
                lightboxModal.classList.add('flex');
                void lightboxModal.offsetWidth; // force reflow
                lightboxModal.classList.remove('opacity-0');
                lightboxImg.classList.remove('scale-95');
                lightboxImg.classList.add('scale-100');
                document.body.style.overflow = 'hidden';
            };

            const lightboxModal = document.getElementById('lightboxModal');
            const lightboxImg = document.getElementById('lightboxImg');
            const closeLightboxBtn = document.getElementById('closeLightboxBtn');
            
            if (lightboxModal && closeLightboxBtn) {
                window.closeLightbox = function() {
                    lightboxModal.classList.add('opacity-0');
                    lightboxImg.classList.remove('scale-100');
                    lightboxImg.classList.add('scale-95');
                    setTimeout(() => {
                        lightboxModal.classList.add('hidden');
                        lightboxModal.classList.remove('flex');
                        const mainModal = document.getElementById('fullGalleryModal');
                        if (mainModal && mainModal.classList.contains('hidden')) {
                            document.body.style.overflow = '';
                        }
                    }, 300);
                };

                closeLightboxBtn.addEventListener('click', window.closeLightbox);
                lightboxModal.addEventListener('click', window.closeLightbox);
            }
"""

new_global_js = """
    </script>
    <script>
        // Bulletproof Global Lightbox logic
        window.openLightbox = function(src) {
            const lightboxModal = document.getElementById('lightboxModal');
            const lightboxImg = document.getElementById('lightboxImg');
            if (!lightboxModal || !lightboxImg) return;
            
            lightboxImg.src = src;
            lightboxModal.classList.remove('hidden');
            lightboxModal.classList.add('flex');
            void lightboxModal.offsetWidth; // force reflow
            lightboxModal.classList.remove('opacity-0');
            lightboxImg.classList.remove('scale-95');
            lightboxImg.classList.add('scale-100');
            document.body.style.overflow = 'hidden';
        };

        window.closeLightbox = function() {
            const lightboxModal = document.getElementById('lightboxModal');
            const lightboxImg = document.getElementById('lightboxImg');
            if (!lightboxModal || !lightboxImg) return;
            
            lightboxModal.classList.add('opacity-0');
            lightboxImg.classList.remove('scale-100');
            lightboxImg.classList.add('scale-95');
            setTimeout(() => {
                lightboxModal.classList.add('hidden');
                lightboxModal.classList.remove('flex');
                const mainModal = document.getElementById('fullGalleryModal');
                if (mainModal && mainModal.classList.contains('hidden')) {
                    document.body.style.overflow = '';
                }
            }, 300);
        };
    </script>
"""

# Find where to replace the old JS
if old_js in content:
    content = content.replace(old_js, "")
    # Insert new_global_js at the end before </body>
    content = content.replace("</body>", new_global_js + "\n</body>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied hero contrast and foolproof mobile lightbox updates!")
