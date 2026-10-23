# Florescer para Android

Aplicativo Android que inclui a interface de `app/` em uma WebView local. Funciona sem servidor e sem permissão de internet. O build copia os três arquivos web e remove apenas a importação de fontes externas da cópia; os originais permanecem intactos.

## Abrir e compilar

Abra esta pasta no Android Studio. Use JDK 17 ou 21, SDK Android 35 e Build Tools 35.0.0. O Android Studio pode instalar esses componentes e solicitar a aceitação das licenças.

```sh
./gradlew assembleDebug lintDebug
```

APK de teste: `app/build/outputs/apk/debug/app-debug.apk`. Para instalar com um aparelho conectado e depuração USB ativada:

```sh
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Compatível com Android 8.0 ou superior. Mantenha o Android System WebView atualizado.

## Funcionamento e dados

O check-in e o diário são armazenados no armazenamento local da WebView, dentro dos dados privados do aplicativo. Os registros do site no navegador não são importados. Não há sincronização, conta ou backup automático; desinstalar o app ou limpar seus dados apaga os registros. Os dados não recebem criptografia adicional pelo aplicativo.

Os links de apoio abrem o discador, sem realizar ligações automaticamente. Não são solicitadas permissões de telefone. A confirmação para excluir registros é exibida por um diálogo Android.

## Validação em dispositivo

Após instalar, salve um check-in e uma entrada no diário, feche e reabra o app e confirme a persistência. Teste o limite de quatro sentimentos, a exclusão, a pausa de respiração e a abertura do discador. Confira também o teclado e as barras do sistema. Compilar e passar no lint não substitui esses testes em um aparelho ou emulador.

Para publicar na Play Store, configure uma chave de assinatura de produção e gere um Android App Bundle assinado pelo Android Studio. Não use a chave de debug para distribuição de produção e não versione chaves privadas.

## Neste ambiente cloud

As ferramentas foram instaladas fora do repositório, em `/workspace/android-tools`. Como o diretório pessoal da máquina é somente leitura, use:

```sh
export JAVA_HOME=/workspace/android-tools/jdk-21
export ANDROID_HOME=/workspace/android-tools/sdk
export ANDROID_USER_HOME=/workspace/android-tools/android-user
export GRADLE_USER_HOME=/workspace/android-tools/gradle-home
./gradlew --no-daemon --max-workers=2 assembleDebug lintDebug
```

A chave de teste fica em `.local/debug.keystore` e não é versionada. Nunca a use como chave de publicação.
