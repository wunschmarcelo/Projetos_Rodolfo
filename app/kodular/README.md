# Florescer no Kodular

Esta pasta contém os assets adaptados para montar o projeto no Kodular. Não é um projeto `.aia` importável e ainda não foi validada no Kodular Companion ou em APK gerado pelo Kodular.

1. No Kodular Creator, crie o projeto `Florescer`.
2. Em Screen1, oculte a barra de título, use orientação Portrait e desative Scrollable. Escolha o layout responsivo.
3. Adicione um Web Viewer chamado `Web_Viewer1`, com largura e altura Fill Parent. Habilite JavaScript, se essa propriedade estiver disponível.
4. Envie os três arquivos da pasta `assets` para a mídia do projeto, preservando os nomes.
5. No evento `Screen1.Initialize`, chame `Web_Viewer1.GoToUrl` com `file:///android_asset/index.html`.
6. Adicione um Activity Starter. No evento `Web_Viewer1.WebViewStringChange`, aceite somente os valores `tel:188` e `tel:192`; configure Action como `android.intent.action.DIAL`, DataUri como o valor recebido e chame StartActivity. Isso abre o discador; não use ACTION_CALL.
7. No evento `Screen1.BackPressed`, se Web_Viewer1.CanGoBack for verdadeiro chame GoBack; caso contrário, feche a tela ou exiba uma confirmação.
8. Gere um APK pelo menu de exportação do Kodular e teste no aparelho. O caminho de assets pode diferir no Companion: valide principalmente no APK exportado.

Os registros usam localStorage da WebView e não são compartilhados com o navegador ou com o APK Android Studio. Esta versão dispensa fontes externas e inclui alternativa para gerar IDs em origens locais sem crypto.randomUUID.

## Verificação necessária no APK Kodular

Salve check-in e diário; feche e reabra o app para confirmar a persistência. Teste a exclusão de registros (diálogo confirm), limite de sentimentos, pausa de respiração, teclado, botão voltar e a abertura do discador. Não considere a persistência validada apenas pelo Companion. Limpar dados ou desinstalar pode apagar os registros. O armazenamento não possui criptografia adicional.
