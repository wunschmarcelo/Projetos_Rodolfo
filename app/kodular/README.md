# Florescer — projeto para Kodular

O arquivo pronto para importação é `app/entregas/Florescer.aia`. Ele é diferente do ZIP antigo de assets: contém a tela Screen1, componentes, blocos e os arquivos da interface.

## Importar

1. Acesse https://creator.kodular.io e entre na sua conta.
2. No menu Projects (Projetos), escolha Import project (.aia) from my computer.
3. Selecione `Florescer.aia` no computador. Não descompacte o arquivo e não use o ZIP antigo.
4. Abra Screen1. No Designer devem aparecer WebViewer1, ActivityStarter1 e Notifier1.
5. Em Blocks, os eventos Initialize, WebViewStringChange, BackPressed, AfterChoosing e ErrorOccurred já estão configurados.
6. Use o menu Export para gerar o APK e instale no celular Android. O Kodular pode solicitar ajustes conforme sua versão atual e as políticas de geração de APK.

## O que está incluído

- Interface de check-in, energia, ansiedade, sentimentos, diário e respiração.
- Arquivos locais: não precisa de servidor ou de fontes externas.
- Inicialização automática da página no WebViewer.
- Integração dos links 188 e 192 com o discador por ActivityStarter, sem efetuar ligações automaticamente.
- Botão voltar: fecha apoio, retorna ao check-in ou pede confirmação para sair.
- Armazenamento local da WebView, com alternativa de geração de IDs para origens locais.

## Limites e validação

O pacote foi gerado no formato padrão AIA e sua estrutura ZIP, JSON da tela e XML dos blocos foram verificados. A interface e a ponte JavaScript foram testadas em Chromium com uma ponte simulada. A importação no Kodular Creator, o Companion e o APK gerado pelo Kodular ainda não foram executados neste ambiente; essa validação depende do serviço externo. O pacote não contém extensões de terceiros.

No APK gerado, teste: salvar e reabrir check-in e diário; excluir registro; selecionar até quatro sentimentos; iniciar e encerrar respiração; abrir o discador; usar voltar e verificar o teclado. O Companion pode usar um caminho de assets diferente de `file:///android_asset/index.html`; valide o APK exportado antes de concluir que o caminho está quebrado.

Os registros não são compartilhados com o site ou com o APK feito pelo Android Studio. Não há conta, sincronização nem criptografia adicional pelo app. Limpar os dados da aplicação ou desinstalá-la pode apagar os registros. Confira as configurações de backup do Kodular antes de distribuir o aplicativo.

## Atualizar o projeto

Edite a interface em `assets/` ou os blocos em `build_project.py`, depois execute:

```sh
python3 app/kodular/build_project.py
```

O script atualiza os fontes da tela em `project/` e gera novamente `app/entregas/Florescer.aia`. Importe o arquivo atualizado como um novo projeto ou preserve uma cópia do projeto anterior no Kodular antes de substituí-lo.
