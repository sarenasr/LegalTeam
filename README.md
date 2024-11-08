# LegalTeam

**LegalTeam** es una aplicación web para abogados en Colombia que facilita el seguimiento de actualizaciones en casos legales, proporcionando notificaciones en tiempo real y análisis de documentos relevantes utilizando un modelo de lenguaje adaptado al sistema legal colombiano.

## Funcionalidades

1. **Seguimiento Automático de Casos:** Scraper que monitoriza casos legales y actualiza a los usuarios cuando hay novedades.
2. **Notificaciones:** Envío de notificaciones por correo electrónico o SMS sobre cualquier cambio en los casos.
3. **Análisis de Documentos:** Un modelo de lenguaje (LLM) finetuneado en legislación colombiana que proporciona resúmenes y destaca información clave en documentos legales.

## Estructura del Proyecto

- **LegalTeam/** - Configuraciones generales del proyecto Django.
- **scraper/** - Scripts y tareas de scraping para la monitorización de casos.
- **notifications/** - Configuración de notificaciones para los usuarios.
- **analysis/** - Manejo de la IA y análisis de documentos.
- **frontend/** - (Opcional) Plantillas y archivos estáticos para la interfaz.

## Modelo de Lenguaje Adaptado (LLM)

Este proyecto utiliza un modelo LLM basado en [Modelo Base, e.g., GPT-Neo] finetuneado específicamente para el sistema legal colombiano utilizando NVIDIA Workbench. Esto permite análisis automatizados de documentos legales, como resúmenes y extracción de puntos clave.

## Instalación

1. Clonar el repositorio.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Configurar las variables de entorno en `.env` para las API keys y configuraciones de base de datos.
4. Ejecutar migraciones de base de datos: `python manage.py migrate`.
5. Ejecutar el servidor de desarrollo: `python manage.py runserver`.

## Uso

1. Configurar el scraper para monitorizar casos específicos.
2. Configurar las notificaciones en la sección correspondiente.
3. Subir documentos legales para análisis y revisión de resultados generados por el LLM.

## Contribuir

Si deseas contribuir, por favor, abre un issue o un pull request. Agradecemos cualquier ayuda para mejorar LegalTeam.
