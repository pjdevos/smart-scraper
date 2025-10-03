"""
Browser Fingerprint Masking - Hide automation detection
"""
import random
from typing import Dict, List
from utils.logger import get_logger

logger = get_logger(__name__)


class FingerprintMask:
    """Masks browser fingerprints to avoid detection"""

    # Realistic screen resolutions
    RESOLUTIONS = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
        {'width': 1440, 'height': 900},
        {'width': 2560, 'height': 1440},
        {'width': 1680, 'height': 1050},
    ]

    # Realistic timezone offsets
    TIMEZONES = [
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
        'Europe/London',
        'Europe/Paris',
        'Europe/Berlin',
    ]

    # Realistic languages
    LANGUAGES = [
        ['en-US', 'en'],
        ['en-GB', 'en'],
        ['en-US', 'en', 'es'],
        ['en-GB', 'en', 'fr'],
    ]

    @staticmethod
    def get_random_viewport() -> Dict[str, int]:
        """Get random viewport size"""
        resolution = random.choice(FingerprintMask.RESOLUTIONS)
        return {
            'width': resolution['width'],
            'height': resolution['height']
        }

    @staticmethod
    def get_random_timezone() -> str:
        """Get random timezone"""
        return random.choice(FingerprintMask.TIMEZONES)

    @staticmethod
    def get_random_languages() -> List[str]:
        """Get random language list"""
        return random.choice(FingerprintMask.LANGUAGES)

    @staticmethod
    def get_webgl_vendor() -> str:
        """Get random WebGL vendor"""
        vendors = [
            'Intel Inc.',
            'Google Inc.',
            'NVIDIA Corporation',
            'AMD',
        ]
        return random.choice(vendors)

    @staticmethod
    def apply_stealth_scripts(page) -> bool:
        """
        Apply JavaScript to mask automation (Playwright).

        Args:
            page: Playwright page object

        Returns:
            True if successful
        """
        try:
            if not hasattr(page, 'add_init_script'):
                return False

            # Remove webdriver property
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # Mask Chrome runtime
            page.add_init_script("""
                window.chrome = {
                    runtime: {}
                };
            """)

            # Mock plugins
            page.add_init_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        }
                    ]
                });
            """)

            # Mock permissions
            page.add_init_script("""
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({state: Notification.permission}) :
                        originalQuery(parameters)
                );
            """)

            # Mock languages
            languages = FingerprintMask.get_random_languages()
            page.add_init_script(f"""
                Object.defineProperty(navigator, 'languages', {{
                    get: () => {languages}
                }});
            """)

            # Mock hardware concurrency (CPU cores)
            cores = random.choice([2, 4, 6, 8, 12, 16])
            page.add_init_script(f"""
                Object.defineProperty(navigator, 'hardwareConcurrency', {{
                    get: () => {cores}
                }});
            """)

            # Mock device memory
            memory = random.choice([2, 4, 8, 16])
            page.add_init_script(f"""
                Object.defineProperty(navigator, 'deviceMemory', {{
                    get: () => {memory}
                }});
            """)

            # Mock WebGL vendor
            vendor = FingerprintMask.get_webgl_vendor()
            page.add_init_script(f"""
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) {{
                        return '{vendor}';
                    }}
                    return getParameter.apply(this, arguments);
                }};
            """)

            # Mock battery API
            page.add_init_script("""
                if ('getBattery' in navigator) {
                    delete navigator.getBattery;
                }
            """)

            # Mock connection
            page.add_init_script("""
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        rtt: 50,
                        downlink: 10,
                        saveData: false
                    })
                });
            """)

            logger.debug("Applied stealth scripts to mask fingerprint")
            return True

        except Exception as e:
            logger.warning(f"Error applying stealth scripts: {e}")
            return False

    @staticmethod
    def randomize_canvas_fingerprint(page) -> bool:
        """
        Randomize canvas fingerprint (Playwright).

        Args:
            page: Playwright page object

        Returns:
            True if successful
        """
        try:
            if not hasattr(page, 'add_init_script'):
                return False

            # Add noise to canvas fingerprint
            noise = random.uniform(0.00001, 0.0001)

            page.add_init_script(f"""
                const toDataURL = HTMLCanvasElement.prototype.toDataURL;
                const toBlob = HTMLCanvasElement.prototype.toBlob;
                const getImageData = CanvasRenderingContext2D.prototype.getImageData;

                const noisify = function(canvas, context) {{
                    if (!context) {{
                        return;
                    }}

                    const shift = {{
                        'r': Math.floor(Math.random() * 10) - 5,
                        'g': Math.floor(Math.random() * 10) - 5,
                        'b': Math.floor(Math.random() * 10) - 5,
                        'a': Math.floor(Math.random() * 10) - 5
                    }};

                    const width = canvas.width;
                    const height = canvas.height;

                    if (width && height) {{
                        const imageData = context.getImageData(0, 0, width, height);
                        for (let i = 0; i < height; i++) {{
                            for (let j = 0; j < width; j++) {{
                                const n = ((i * (width * 4)) + (j * 4));
                                imageData.data[n + 0] = imageData.data[n + 0] + shift.r;
                                imageData.data[n + 1] = imageData.data[n + 1] + shift.g;
                                imageData.data[n + 2] = imageData.data[n + 2] + shift.b;
                                imageData.data[n + 3] = imageData.data[n + 3] + shift.a;
                            }}
                        }}
                        context.putImageData(imageData, 0, 0);
                    }}
                }};

                HTMLCanvasElement.prototype.toDataURL = function() {{
                    noisify(this, this.getContext('2d'));
                    return toDataURL.apply(this, arguments);
                }};
            """)

            logger.debug("Randomized canvas fingerprint")
            return True

        except Exception as e:
            logger.warning(f"Error randomizing canvas: {e}")
            return False