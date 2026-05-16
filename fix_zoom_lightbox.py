import sys
import re

file_path = "d:\\ANTIGRAVITYFILESME\\GARAGEDOORSLEADS\\noahgaragedoors\\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix BEFORE17 to be static zoom
old_before17 = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover scale-[1.25] origin-[50%_75%] hover:scale-[1.3] transition-transform duration-300">'''
new_before17 = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover scale-[1.15] origin-[50%_75%] cursor-pointer" onclick="openLightbox(this.src)">'''
content = content.replace(old_before17, new_before17)

# Make sure to replace any other instances just in case
old_before17_fallback = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover">'''
new_before17_fallback = '''<img src="gallery/BEFORE17.jpeg" alt="Old garage door before replacement San Diego" class="w-full h-full object-cover scale-[1.15] origin-[50%_75%] cursor-pointer" onclick="openLightbox(this.src)">'''
content = content.replace(old_before17_fallback, new_before17_fallback)

# 2. Add onclick to all gallery images
def add_onclick(match):
    img_tag = match.group(0)
    if 'BEFORE17' in img_tag:
        return img_tag # Already handled
    
    # Add cursor-pointer and onclick
    if 'cursor-pointer' not in img_tag:
        img_tag = img_tag.replace('class="', 'class="cursor-pointer ')
    if 'onclick=' not in img_tag:
        img_tag = img_tag.replace('class="', 'onclick="openLightbox(this.src)" class="')
    return img_tag

# Only replace in gallery sections
# We'll just replace ALL images in the gallery folder that don't have onclick
content = re.sub(r'<img src="gallery/[^>]+>', add_onclick, content)

# 3. Define openLightbox globally
# Remove the old JS logic
old_js = """
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

new_js = """
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

content = content.replace(old_js, new_js)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied static zoom, global lightbox, and inline onclicks!")
