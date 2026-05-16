import sys

file_path = "d:\\ANTIGRAVITYFILESME\\GARAGEDOORSLEADS\\noahgaragedoors\\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update BEFORE17 images to zoom in
# Showcase version
old_before17_showcase = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover">
                                <span class="absolute bottom-3 left-3 text-xs font-black uppercase bg-red-600 text-white px-3 py-1 rounded-full shadow-lg">Before</span>'''
new_before17_showcase = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover scale-[1.25] origin-[50%_75%] hover:scale-[1.3] transition-transform duration-300">
                                <span class="absolute bottom-3 left-3 text-xs font-black uppercase bg-red-600 text-white px-3 py-1 rounded-full shadow-lg">Before</span>'''

content = content.replace(old_before17_showcase, new_before17_showcase)

# Modal version
old_before17_modal = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover">
                                    <span class="absolute bottom-2 left-2 text-[11px] font-black uppercase bg-red-600 text-white px-2 py-0.5 rounded-full">Before</span>'''
new_before17_modal = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover scale-[1.25] origin-[50%_75%] hover:scale-[1.3] transition-transform duration-300">
                                    <span class="absolute bottom-2 left-2 text-[11px] font-black uppercase bg-red-600 text-white px-2 py-0.5 rounded-full">Before</span>'''

content = content.replace(old_before17_modal, new_before17_modal)


# 2. Add Lightbox HTML
lightbox_html = """
        <!-- LIGHTBOX MODAL -->
        <div id="lightboxModal" class="fixed inset-0 z-[200] w-screen h-screen bg-black/95 hidden flex-col items-center justify-center opacity-0 transition-opacity duration-300">
            <button id="closeLightboxBtn" class="absolute top-6 right-6 p-3 bg-white/10 hover:bg-white/20 text-white rounded-full transition-colors z-[210]">
                <i data-lucide="x" class="w-6 h-6"></i>
            </button>
            <div class="w-full h-full p-4 flex items-center justify-center">
                <img id="lightboxImg" src="" alt="Enlarged view" class="max-w-full max-h-full object-contain transform scale-95 transition-transform duration-300">
            </div>
        </div>
"""

# Insert before <!-- FOOTER -->
content = content.replace("        <!-- FOOTER -->", lightbox_html + "\n        <!-- FOOTER -->")


# 3. Add Lightbox JS
lightbox_js = """
            // Lightbox logic
            const lightboxModal = document.getElementById('lightboxModal');
            const lightboxImg = document.getElementById('lightboxImg');
            const closeLightboxBtn = document.getElementById('closeLightboxBtn');
            
            if (lightboxModal && lightboxImg && closeLightboxBtn) {
                // Attach click to all gallery images
                document.querySelectorAll('#gallery img, #fullGalleryModalInner img').forEach(img => {
                    img.classList.add('cursor-pointer');
                    
                    img.addEventListener('click', (e) => {
                        e.stopPropagation(); // prevent other clicks
                        lightboxImg.src = img.src;
                        lightboxModal.classList.remove('hidden');
                        lightboxModal.classList.add('flex');
                        void lightboxModal.offsetWidth; // force reflow
                        lightboxModal.classList.remove('opacity-0');
                        lightboxImg.classList.remove('scale-95');
                        lightboxImg.classList.add('scale-100');
                        document.body.style.overflow = 'hidden';
                    });
                });

                function closeLightbox() {
                    lightboxModal.classList.add('opacity-0');
                    lightboxImg.classList.remove('scale-100');
                    lightboxImg.classList.add('scale-95');
                    setTimeout(() => {
                        lightboxModal.classList.add('hidden');
                        lightboxModal.classList.remove('flex');
                        // Only restore overflow if the main gallery modal isn't open
                        const mainModal = document.getElementById('fullGalleryModal');
                        if (mainModal && mainModal.classList.contains('hidden')) {
                            document.body.style.overflow = '';
                        }
                    }, 300);
                }

                closeLightboxBtn.addEventListener('click', closeLightbox);
                lightboxModal.addEventListener('click', (e) => {
                    // close if clicking anywhere on the background or image
                    closeLightbox();
                });
            }
"""

# Find the closing tag of the event listener inside our custom JS
# The existing JS looks like this:
#                 modal.addEventListener('click', (e) => {
#                     if (e.target === modal) {
#                         closeModal();
#                     }
#                 });
#             }
#         });
#     </script>

js_insert_point = "                });\n            }"
content = content.replace(js_insert_point, js_insert_point + "\n" + lightbox_js)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied lightbox and zoom updates!")
