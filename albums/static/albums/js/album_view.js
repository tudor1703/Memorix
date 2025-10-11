function goBack() {
    // Check if there's a referrer (page that sent us here)
    if (document.referrer && document.referrer !== window.location.href) {
        window.location.href = document.referrer;
    } else {
        // Fallback to browser's back button
        window.history.back();
    }
}