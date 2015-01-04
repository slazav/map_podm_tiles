Проект по созданию тайлового кеша карт Подмосковья ([Исходный репозиторий](https://github.com/slazav/map_podm), [Готовые листы](http://slazav.mccme.ru/maps/podm/index.htm)).

### Требования
Для создания тайлов требуются следующие компоненты:
  * [MapSoft](https://github.com/ushakov/mapsoft)
  * ImageMagic
  * Node.js
  * Собственно [репозиторий с картами](https://github.com/slazav/map_podm)
 
### Запуск тайлинга
  0. Сгенерируйте палитру:

  ```
  cd palette
  ./gen_palette
  ```

  0. Проинсталлируйте зависимости для обрезки тайлов по границе

  ```
  cd editborder
  npm i
  ```

  0. Подправьте пути в конфигах `settings_full.sh` и `settings_border.sh`.
  0. Сгенерируйте `fig` файлы

  ```
  ./update_fig
  ```

  0. Сгенерируйте собственно растровые тайлы

  ```
  ./update_png <settings_file>
  ```

### Примечания
  * Есть два конфига: `settings_border.sh` для правки границы (зумы 9-11) и `settings_full.sh` для полноценного тайлинга (зумы 9-14)
  * Для редактирования границы есть небольшая страничка `editborder/index.html` (нужно запустить серверную часть `editborder/border_server.js` на Node.js)
  * Все тайлы палитровые и используют общую палитру
