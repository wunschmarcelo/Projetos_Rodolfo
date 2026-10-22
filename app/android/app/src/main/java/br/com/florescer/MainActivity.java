package br.com.florescer;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.*;
import android.view.View;
import android.view.WindowInsets;
import java.io.IOException;

public class MainActivity extends Activity {
    private WebView webView;
    private static final String HOST = "appassets.androidplatform.net";
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(255,252,244));
        setContentView(webView);
        webView.setOnApplyWindowInsetsListener((view, insets) -> {
            if (android.os.Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.ime());
                view.setPadding(bars.left, bars.top, bars.right, bars.bottom);
            } else {
                view.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(), insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            }
            return insets;
        });
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setAllowFileAccess(false);
        webView.getSettings().setAllowContentAccess(false);
        webView.getSettings().setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        webView.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String path = uri.getPath();
                if ("https".equals(uri.getScheme()) && HOST.equals(uri.getHost()) && path != null) {
                    String file = path.equals("/") ? "index.html" : path.substring(1);
                    if (file.equals("index.html") || file.equals("style.css") || file.equals("script.js")) {
                        try { return new WebResourceResponse(file.endsWith("css") ? "text/css" : file.endsWith("js") ? "application/javascript" : "text/html", "UTF-8", getAssets().open(file)); }
                        catch (IOException ignored) { }
                    }
                }
                return new WebResourceResponse("text/plain", "UTF-8", 404, "Not Found", java.util.Collections.emptyMap(), new java.io.ByteArrayInputStream(new byte[0]));
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (HOST.equals(uri.getHost()) && "https".equals(uri.getScheme())) return false;
                if ("tel".equals(uri.getScheme())) {
                    try { startActivity(new Intent(Intent.ACTION_DIAL, uri)); }
                    catch (ActivityNotFoundException e) { new AlertDialog.Builder(MainActivity.this).setMessage("Não há discador disponível neste aparelho.").setPositiveButton("OK", null).show(); }
                }
                return true;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onJsConfirm(WebView view, String url, String message, JsResult result) {
                new AlertDialog.Builder(MainActivity.this).setMessage(message).setPositiveButton("Excluir", (d,w)->result.confirm()).setNegativeButton("Cancelar", (d,w)->result.cancel()).setOnCancelListener(d->result.cancel()).show();
                return true;
            }
        });
        webView.loadUrl("https://" + HOST + "/index.html");
    }
    @Override public void onBackPressed() {
        webView.evaluateJavascript("(() => {const d=document.querySelector('dialog[open]');if(d){d.close();return true;}return false;})()", value -> { if (!"true".equals(value)) finish(); });
    }
    @Override protected void onDestroy() { if(webView != null) {webView.destroy();} super.onDestroy(); }
}
