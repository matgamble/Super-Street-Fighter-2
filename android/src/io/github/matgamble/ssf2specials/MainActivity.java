package io.github.matgamble.ssf2specials;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.webkit.ValueCallback;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/**
 * Zeigt die Specials-Seite aus assets/index.html.
 *
 * Die Seite ist vollständig eingebettet – die App braucht kein Netz und darum
 * auch keine einzige Berechtigung.
 */
public class MainActivity extends Activity {

    private WebView web;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        // Beim Spielen soll der zweite Screen nicht nach kurzer Zeit ausgehen.
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        web = new WebView(this);
        // Farbe des Seitenhintergrunds, damit beim Start nichts weiß aufblitzt.
        web.setBackgroundColor(0xFF0C0A1A);
        web.setWebViewClient(new WebViewClient());

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);   // localStorage: merkt sich Charakter und Ansicht
        s.setAllowFileAccess(true);
        s.setUseWideViewPort(true);     // das viewport-Meta der Seite gilt
        s.setLoadWithOverviewMode(false);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        // Systemweite Schriftvergrößerung ignorieren – die Seite skaliert selbst,
        // sonst würde sie zweimal skaliert und passte nicht mehr auf den Screen.
        s.setTextZoom(100);

        setContentView(web);

        if (state == null) {
            web.loadUrl("file:///android_asset/index.html");
        } else {
            web.restoreState(state);
        }
    }

    /**
     * Die Zurück-Taste des Geräts geht erst innerhalb der Seite zurück –
     * offene Charakterauswahl schließen, dann zum Titelbildschirm. Erst wenn
     * dort nichts mehr zurückzugehen ist, wird die App beendet.
     *
     * Bewusst eine anonyme Klasse statt eines Lambdas: der hier benutzte Dexer
     * (dx) übersetzt invokedynamic nicht.
     */
    @Override
    public void onBackPressed() {
        web.evaluateJavascript(
                "(window.__back && window.__back()) ? 'ja' : 'nein'",
                new ValueCallback<String>() {
                    @Override
                    public void onReceiveValue(String value) {
                        if (value == null || !value.contains("ja")) {
                            finish();
                        }
                    }
                });
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            hideSystemBars();
        }
    }

    /** Status- und Navigationsleiste ausblenden; der Screen ist klein genug. */
    private void hideSystemBars() {
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }
}
