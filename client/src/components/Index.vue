<template>
  <!DOCTYPE HTML>
  <html lang="ru">
      <head>
          <title>КОГБУ "ЦГАКО"</title>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
          <meta name="keywords" content="Ключевые слова, и, фразы, через, запятую">
          <meta name="description" content="Описание контента страницы, 1-2 предложения.">

          <link rel="icon" type="image/png" href="../assets/images/favicon.png">
      </head>

      <body class="is-preload">

          <div class="fullscreen-bg">
            <video loop muted autoplay poster="../assets/images/backvid_poster.png"
            class="fullscreen-bg__video">
              <source src="../assets/images/backvideo.mp4" type="video/mp4">
            </video>
          </div>

          <div id="wrapper" class="fade-in">

              <a id="back-to-top" href="#" class="button icon solo fa-arrow-up hidden"></a>

              <div id="intro">
                  <h1 class="noselect">Центральный государственный архив<br />
                  Кировской области</h1>
                  <p class="noselect">Historia est magistra vita — История - учитель жизни</p>
                  <ul class="actions">
                      <li>
                        <a href="#header"
                        class="button icon solo fa-arrow-down scrolly">
                          Продолжить
                        </a>
                      </li>
                  </ul>
              </div>

              <header id="header">
                  <a href="index.html" class="logo">
                    <img alt="Логотип" class="logo-img" src="../assets/images/favicon3.png"/>
                    <div>
                      Центральный<br/>
                      государственный<br/>
                      архив<br/>
                      Кировской<br/>
                      области<br/>
                      <span>на главную</span>
                    </div>
                  </a>
              </header>
<!--

              <nav id="nav">

                  <ul class="links">
                      <li class="has-sub">
                          <a href="#">Об архиве</a>
                          <ul>
                              <li class="">
                                <a title="Краткая историческая справка" href="#">
                                  Краткая историческая справка
                                </a>
                              </li>
                              <li><a title="Состав фондов" href="#">Состав фондов</a></li>
                              <li><a title="Наши услуги" href="#">Наши услуги</a></li>
                          </ul>
                      </li>
                      <li class="has-sub">
                          <a href="#">События</a>
                          <ul>
                              <li>
                                <a title="Новости архива" href="news_all.html">
                                  Новости архива
                                </a>
                              </li>
                              <li>
                                <a title="Анонсы мероприятий" href="anouncements.html">
                                  Анонсы мероприятий
                                </a>
                              </li>
                          </ul>
                      </li>
                      <li class="has-sub">
                          <a href="#">НСА</a>
                          <ul>
                              <li class="has-sub-sub">
                                  <a title="Электронный архив" href="#">Электронный архив</a>
                                  <ul class="child">
                                      <li class="has-sub-sub">
                                          <a title="Исповедные росписи
                                          церквей Вятской епархии. XVIII – XX вв." href="#">
                                            Исповедные росписи церквей Вятской
                                            епархии. XVIII – XX вв.
                                          </a>
                                          <ul class="child">
                                            <li><a title="Опись 1" href="#">Опись 1</a></li>
                                            <li><a title="Опись 2" href="#">Опись 2</a></li>
                                            <li><a title="Опись 3" href="#">Опись 3</a></li>
                                            <li><a title="Опись 4" href="#">Опись 4</a></li>
                                          </ul>
                                      </li>
                                      <li class="has-sub-sub">
                                          <a title="Клировые ведомости церквей
                                          Вятской епархии. XVIII – XX вв." href="#">
                                            Клировые ведомости церквей Вятской
                                            епархии. XVIII – XX вв.
                                          </a>
                                          <ul class="child">
                                            <li><a title="Опись 1" href="#">Опись 1</a></li>
                                            <li><a title="Опись 2" href="#">Опись 2</a></li>
                                            <li><a title="Опись 3" href="#">Опись 3</a></li>
                                            <li><a title="Опись 4" href="#">Опись 4</a></li>
                                          </ul>
                                      </li>
                                      <li>
                                        <a title="Метрические книги церквей
                                        Вятской епархии. XVIII – XX вв." href="#">
                                        Метрические книги церквей Вятской епархии. XVIII – XX вв.
                                        </a>
                                      </li>
                                      <li>
                                        <a title="Список домохозяев
                                        Вятской губернии на 1891 г." href="#">
                                          Список домохозяев Вятской губернии на 1891 г.
                                        </a>
                                      </li>
                                  </ul>
                              </li>
                              <li class="has-sub-sub">
                                  <a title="" href="#">Описи дел</a>
                                  <ul class="child">
                                      <li><a title="Опись 1" href="#">Опись 1</a></li>
                                      <li><a title="Опись 2" href="#">Опись 2</a></li>
                                      <li><a title="Опись 3" href="#">Опись 3</a></li>
                                      <li><a title="Опись 4" href="#">Опись 4</a></li>
                                  </ul>
                              </li>
                              <li><a title="" href="#">Справочники по фондам</a></li>
                              <li><a title="" href="#">Каталоги, картотеки</a></li>
                          </ul>
                      </li>
                      <li><a href="#">Деятельность</a></li>
                      <li><a href="#">Публикации</a></li>
                      <li><a href="contacts.html">Контакты</a></li>
                  </ul>

                  <ul class="search">
                      <li>
                        <input placeholder="Поиск по сайту"
                        type="text" id="search_fld" class="search_fld">
                      </li>
                  </ul>

                  <ul class="icons">
                      <li class="go-search hidden">
                          <a href="search_result.html"
                          class="search_btn icon fa-arrow-right">
                            <span class="label">
                              Поиск
                            </span>
                          </a>
                      </li>
                      <li>
                        <a href="#" class="search_swt icon fa-search">
                          <span class="label">
                            Открыть/закрыть поисковую строку
                          </span>
                        </a>
                      </li>
                  </ul>

              </nav>
-->

              <nav id="nav">
                <NodeTree :node="menu"></NodeTree>
              </nav>


<!--

              <div id="main">

                  <div class="banners">

                          <div class="slider banner-slider" id="slider">

                              <div class="banner-slide">
                                <a href="generic.html" title="2019 - Год театра в России">
                                  <img src="../assets/images/banner-1.jpg"
                                  class="banner-image noselect">
                                  <section class="banner-desc noselect">
                                    <h4>2019 - Год театра в России</h4>
                                    <p class="line-clamp">
                                      В соответствии с Указом Президента
                                      Владимира Путина 2019 год в Российской
                                      Федерации объявлен Годом театра. Его задачи
                                      связаны с сохранением и популяризацией
                                      отечественных театральных традиций и
                                      достижений; доступностью лучших образцов
                                      театрального искусства для жителей,
                                      совершенствованием организации театрального дела.
                                    </p>
                                  </section>
                                </a>
                              </div>

                              <div class="banner-slide">
                                <a href="generic.html" title="2019 - Год театра в России">
                                  <img src="../assets/images/banner-2.jpg"
                                  class="banner-image noselect">
                                  <section class="banner-desc noselect">
                                      <h4 class="noselect">
                                        100-летие архивной службы РФ
                                      </h4>
                                      <p class="line-clamp noselect">
                                        2018 год – знаменательный год для архивистов.
                                        Государственной архивной службе России
                                        исполнится 100 лет. 1 июня 1918 г.
                                        Совет Народных Комиссаров принял декрет
                                        «О реорганизации и централизации архивного дела в РСФСР».
                                      </p>
                                  </section>
                                </a>
                              </div>

                              <div class="banner-slide">
                                <a href="generic.html" title="2019 - Год театра в России">
                                  <img src="../assets/images/banner-3.jpg"
                                  class="banner-image noselect">
                                  <section class="banner-desc noselect">
                                    <h4 class="noselect">
                                      Фотоконкурс «Время. События. Люди»
                                    </h4>
                                    <p class="line-clamp noselect">
                                      Конкурс фотографий «Время. События. Люди»
                                      организуется с целью дальнейшего пополнения
                                      архивных фондов и сохранения их для грядущих
                                      поколений и в связи с исполняющимся в 2018 году
                                      100-летием государственной архивной службы
                                      России и Кировской области.
                                    </p>
                                  </section>
                                </a>
                              </div>

                              <div class="banner-slide">
                                <a href="generic.html" title="2019 - Год театра в России">
                                  <img src="../assets/images/rusarchives.png"
                                  class="banner-image noselect">
                                  <section class="banner-desc noselect">
                                    <h4 class="noselect">
                                      Фотоконкурс «Время. События. Люди»
                                    </h4>
                                    <p class="line-clamp noselect">
                                      Конкурс фотографий «Время. События. Люди»
                                      организуется с целью дальнейшего пополнения
                                      архивных фондов и сохранения их для грядущих
                                      поколений и в связи с исполняющимся в 2018 году
                                      100-летием государственной архивной службы
                                      России и Кировской области.
                                    </p>
                                  </section>
                                </a>
                              </div>

                          </div>

                  </div>


                  <div class="two-panels">

                      <main class="firstpanel">

                          <div class="header">
                              <h2>Анонсы мероприятий</h2>
                          </div>

                          <section>
                              <h3>
                                11:00, Казанская 16А, Открытие выставки
                                фотографии "Герои среди нас..."
                              </h3>
                              <p>
                                27 декабря 2018 года состоится презентация выставки
                                фотографий Е. А. Глазыриной «Герои среди нас...»,
                                посвященной 76-й годовщине со дня начала
                                Великой Отечественной войны.
                              </p>
                          </section>

                          <div class="header">
                              <h2>Новое в архиве</h2>
                          </div>

                          <section class="posts">

                              <article style="position: relative;text-align: center;
                              padding: 0;height: 25rem;">
                                <a href="generic.html" class="image fit"
                                 style=" width: 100%;height: 100%;">
                                  <img src="http://gaspiko.ru/media/%D0%9A%D0%9E%D0%93%D0%9A%D0%A3%20%C2%AB%D0%93%D0%90%D0%A1%D0%9F%D0%98%20%D0%9A%D0%9E%C2%BB/11.%20%D0%9F.%D0%90.%20%D0%A7%D0%B5%D0%BC%D0%BE%D0%B4%D0%B0%D0%BD%D0%BE%D0%B2%20%D1%81%20%D1%81%D0%BE%D1%82%D1%80%D1%83%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%B0%20%D0%B8%20%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%82%D0%B0%D0%BC%D0%B823112018.JPG"
                                  alt="" style=" width: 100%;height: 100%;margin: auto;
                                  object-fit: cover;opacity: 0.3;">
                                  <header style="position: absolute;top: 50%;left: 50%;
                                  transform: translate(-50%, -50%);width: 100%;">
                                    <span class="date">
                                      Ноябрь 30, 2018
                                      <div>
                                        <span class="icon fa-eye">
                                          100
                                        </span> |
                                        <span class="icon fa-comments-o">
                                          200
                                        </span> |
                                        <span class="icon fa-thumbs-o-up">
                                          300
                                        </span>
                                      </div>
                                    </span>
                                    <h2 class="line-clamp">
                                      НАГРАЖДЕНИЕ АРХИВА ПО ИТОГАМ
                                      КОНКУРСА «ВЕЛИКИЙ ШАЛЯПИН»
                                    </h2>
                                  </header>
                                </a>
                              </article>

                              <article style="position: relative;text-align: center;
                              padding: 0;height: 25rem;">
                                <a href="generic.html" class="image fit"
                                style=" width: 100%;height: 100%;">
                                  <img src="http://gaspiko.ru/media/%D0%9A%D0%9E%D0%93%D0%9A%D0%A3%20%C2%AB%D0%93%D0%90%D0%A1%D0%9F%D0%98%20%D0%9A%D0%9E%C2%BB/%D0%9D%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%20%D0%91%D0%BE%D1%80%D0%B8%D1%81%20%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B5%D0%B2%D0%B8%D1%87%2C%20%D0%BF%D0%BE%D0%BB%D0%B8%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%2C%20%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D0%B5%D0%BB%D1%8C.jpg"
                                  alt="" style=" width: 100%;height: 100%;margin: auto;
                                  object-fit: cover;opacity: 0.3;">

                                  <header style="position: absolute;top: 50%;
                                  left: 50%;transform: translate(-50%, -50%);width: 100%;">
                                    <span class="date">
                                      Ноябрь 30, 2018
                                      <div>
                                        <span class="icon fa-eye">
                                          100
                                        </span> |
                                        <span class="icon fa-comments-o">
                                          200
                                        </span> |
                                        <span class="icon fa-thumbs-o-up">
                                          300
                                        </span>
                                      </div>
                                    </span>
                                    <h2 class="line-clamp">
                                      НАГРАЖДЕНИЕ АРХИВА ПО ИТОГАМ
                                      КОНКУРСА «ВЕЛИКИЙ ШАЛЯПИН»
                                    </h2>
                                  </header>
                                </a>
                              </article>

                              <article>
                                  <header>
                                      <span class="date">
                                        Ноябрь 30, 2018
                                        <div>
                                          <span class="icon fa-eye">
                                            100
                                          </span> |
                                          <span class="icon fa-comments-o">
                                            200
                                          </span> |
                                          <span class="icon fa-thumbs-o-up">
                                            300
                                          </span>
                                        </div>
                                      </span>
                                      <h2 class="line-clamp">
                                        <a href="generic.html">
                                          НАГРАЖДЕНИЕ АРХИВА ПО ИТОГАМ
                                          КОНКУРСА «ВЕЛИКИЙ ШАЛЯПИН»
                                        </a>
                                      </h2>
                                  </header>

                                  <p class="line-clamp">
                                    21 ноября 2018 года состоялось подведение
                                    итогов межрегионального конкурса исследовательских
                                    работ «Великий Шаляпин», организованного
                                    «Шаляпинской гостиной» при поддержке Вятского
                                    Шаляпинского общества.
                                  </p>
                                  <ul class="actions special">
                                    <li>
                                      <a href="generic.html" class="button">
                                        Смотреть полностью
                                      </a>
                                    </li>
                                  </ul>
                              </article>
                              <article>
                                  <header>
                                      <span class="date">
                                        Ноябрь 30, 2018
                                        <div>
                                          <span class="icon fa-eye">
                                            100
                                          </span> |
                                          <span class="icon fa-comments-o">
                                            200
                                          </span> |
                                          <span class="icon fa-thumbs-o-up">
                                            300
                                          </span>
                                        </div>
                                      </span>
                                      <h2 class="line-clamp">
                                        <a href="generic.html">
                                          УЧАСТИЕ ЦГАКО В ВЫСТАВКЕ ДОКУМЕНТОВ
                                          ПО ИСТОРИИ ПРОФСОЮЗНОГО ДВИЖЕНИЯ КИРОВСКОЙ ОБЛАСТИ
                                        </a>
                                      </h2>
                                  </header>

                                  <p class="line-clamp">
                                    16 ноября 2018 года в Вятской филармонии
                                    г. Кирова прошло торжественное мероприятие,
                                    посвященное 70-летию со дня образования объединения
                                    профсоюзов Кировской области.
                                  </p>
                                  <ul class="actions special">
                                    <li>
                                      <a href="generic.html" class="button">
                                        Смотреть полностью
                                      </a>
                                    </li>
                                  </ul>
                              </article>
                              <article>
                                  <header>
                                      <span class="date">
                                        Ноябрь 30, 2018
                                        <div>
                                          <span class="icon fa-eye">
                                            100
                                          </span> |
                                          <span class="icon fa-comments-o">
                                            200
                                          </span> |
                                          <span class="icon fa-thumbs-o-up">
                                            300
                                          </span>
                                        </div>
                                      </span>
                                      <h2 class="line-clamp">
                                        <a href="generic.html">
                                          ПРЕЗЕНТАЦИЯ «ПИСЕМ С ВОЙНЫ»
                                          В БИБЛИОТЕКЕ ИМ. А.С. ГРИНА
                                        </a>
                                      </h2>
                                  </header>

                                  <a href="generic.html" class="image fit"><img src="http://gaspiko.ru/media/%D0%9A%D0%9E%D0%93%D0%9A%D0%A3%20%C2%AB%D0%93%D0%90%D0%A1%D0%9F%D0%98%20%D0%9A%D0%9E%C2%BB/11.%20%D0%9F.%D0%90.%20%D0%A7%D0%B5%D0%BC%D0%BE%D0%B4%D0%B0%D0%BD%D0%BE%D0%B2%20%D1%81%20%D1%81%D0%BE%D1%82%D1%80%D1%83%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%B0%20%D0%B8%20%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%82%D0%B0%D0%BC%D0%B823112018.JPG" alt="" /></a>
                                  <ul class="actions special">
                                    <li>
                                      <a href="generic.html" class="button">
                                        Смотреть полностью
                                      </a>
                                    </li>
                                  </ul>
                              </article>
                              <article>
                                  <header>
                                      <span class="date">
                                        Ноябрь 30, 2018
                                        <div>
                                          <span class="icon fa-eye">
                                            100
                                          </span> |
                                          <span class="icon fa-comments-o">
                                            200
                                          </span> |
                                          <span class="icon fa-thumbs-o-up">
                                            300
                                          </span>
                                        </div>
                                      </span>
                                      <h2 class="line-clamp">
                                        <a href="generic.html">
                                          ПРИЕМ НА ХРАНЕНИЕ ФОНДОВ ЛИЧНОГО ПРОИСХОЖДЕНИЯ
                                        </a>
                                      </h2>
                                  </header>

                                  <a href="generic.html" class="image fit"><img src="http://gaspiko.ru/media/%D0%9A%D0%9E%D0%93%D0%9A%D0%A3%20%C2%AB%D0%93%D0%90%D0%A1%D0%9F%D0%98%20%D0%9A%D0%9E%C2%BB/%D0%9D%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%20%D0%91%D0%BE%D1%80%D0%B8%D1%81%20%D0%9D%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B5%D0%B2%D0%B8%D1%87%2C%20%D0%BF%D0%BE%D0%BB%D0%B8%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%2C%20%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D0%B5%D0%BB%D1%8C.jpg" alt="" /></a>
                                  <ul class="actions special">
                                    <li>
                                      <a href="generic.html" class="button">
                                        Смотреть полностью
                                      </a>
                                    </li>
                                  </ul>
                              </article>
                              <article>
                                  <header>
                                      <span class="date">
                                        Ноябрь 30, 2018
                                        <div>
                                          <span class="icon fa-eye">
                                            100
                                          </span> |
                                          <span class="icon fa-comments-o">
                                            200
                                          </span> |
                                          <span class="icon fa-thumbs-o-up">
                                            300
                                          </span>
                                        </div>
                                      </span>
                                      <h2 class="line-clamp">
                                        <a href="generic.html">
                                          «КРАЕВЕДЧЕСКИЙ ЧЕТВЕРГ» В ЧЕСТЬ 80-ЛЕТИЯ
                                          КИРОВСКОГО ПАРТАРХИВА
                                        </a>
                                      </h2>
                                  </header>

                                  <a href="generic.html" class="image fit"><img src="http://gaspiko.ru/media/%D0%9A%D0%9E%D0%93%D0%9A%D0%A3%20%C2%AB%D0%93%D0%90%D0%A1%D0%9F%D0%98%20%D0%9A%D0%9E%C2%BB/11.%20%D0%92%D1%8B%D1%81%D1%82%D1%83%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%92.%D0%A1.%20%D0%96%D0%B0%D1%80%D0%B0%D0%B2%D0%B8%D0%BD%D0%B023112018.JPG" alt="" /></a>
                                  <ul class="actions special">
                                      <li>
                                        <a href="generic.html" class="button">
                                          Смотреть полностью
                                        </a>
                                      </li>
                                  </ul>
                              </article>
                              <article>
                                  <header>
                                      <span class="date">
                                        Ноябрь 30, 2018
                                        <div>
                                          <span class="icon fa-eye">
                                            100
                                          </span> |
                                          <span class="icon fa-comments-o">
                                            200
                                          </span> |
                                          <span class="icon fa-thumbs-o-up">
                                            300
                                          </span>
                                        </div>
                                      </span>
                                      <h2 class="line-clamp">
                                        <a href="generic.html">
                                          ЗАНЯТИЕ В ФОРМЕ ЭКСКУРСИИ И ПРЕЗЕНТАЦИИ
                                          ДЛЯ УЧАСТНИКОВ ТВОРЧЕСКОЙ ЛАБОРАТОРИИ
                                        </a>
                                      </h2>
                                  </header>

                                  <a href="generic.html" class="image fit"><img src="http://gaspiko.ru/media/%D0%9A%D0%9E%D0%93%D0%9A%D0%A3%20%C2%AB%D0%93%D0%90%D0%A1%D0%9F%D0%98%20%D0%9A%D0%9E%C2%BB/5.%20%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%BD%D0%B8%D0%BA%D0%B8%20%D1%82%D0%B2%D0%BE%D1%80%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9%20%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%B8%D0%B8%20%D1%81%20%D1%81%D0%BE%D1%82%D1%80%D1%83%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%BE%D1%82%D0%B4%D0%B5%D0%BB%D0%B0%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%92.%D0%A1.%20%D0%96%D0%B0%D1%80%D0%B0%D0%B2%D0%B8%D0%BD%D1%8B%D0%BC%20%D0%B8%20%D0%9B.%D0%93.%20%D0%9F%D0%BE%D0%BF%D1%86%D0%BE%D0%B2%D0%BE%D0%B922112018.JPG" alt="" /></a>
                                  <ul class="actions special">
                                      <li>
                                        <a href="generic.html" class="button">
                                          Смотреть полностью
                                        </a>
                                      </li>
                                  </ul>
                              </article>
                          </section>
                      </main>

                      <div class="secondPanel">
                          <aside id="history-dates">
                              <h3>Памятные даты истории России:</h3>
                              <div class="box">
                                  <span class="history-date-time">
                                      Сегодня (74 года)
                                  </span>
                                  <h4>Памятная дата военной истории России</h4>
                                  <p>
                                    В этот день в 1945 году на Эльбе произошла встреча
                                    советских и американских войск.
                                    Рукопожатие на Эльбе стало символом
                                    братства по оружию стран, вместе сражавшихся
                                    с нацистской Германией. Остатки вермахта теперь были
                                    расколоты на две части — северную и южную.
                                  </p>
                              </div>
                          </aside>
                      </div>

                  </div>

                  <section>
                      <h4>Дополнительный блок</h4>
                  </section>

              </div>
-->

<!--

              <footer id="footer">
                  <section>
                      <h4>Обратная связь</h4>
                      <form method="post" action="#">
                          <div class="fields">
                              <div class="field">
                                  <label for="name">Ваше имя</label>
                                  <input type="text" name="name" id="name" />
                              </div>
                              <div class="field">
                                  <label for="email">Email</label>
                                  <input type="text" name="email" id="email" />
                              </div>
                              <div class="field">
                                  <label for="message">Ваше сообщение</label>
                                  <textarea name="message" id="message" rows="3"></textarea>
                              </div>
                          </div>
                          <ul class="actions">
                              <li><input type="submit" value="Отправить сообщение" /></li>
                          </ul>
                      </form>
                  </section>
                  <section class="contact">
                      <h4>Контактная информация</h4>

                      <h3>Адрес</h3>
                      <p>
                        Юридический адрес (главный корпус): 610027,
                        г. Киров, ул. Карла Маркса, д. 142
                      </p>

                      <h3>Телефон</h3>
                      <p><a href="#">+7 (8332) 357-556</a></p>

                      <h3>Email</h3>
                      <p><a href="#">info@cgako.ru</a></p>

                      <h3>Соц. сети</h3>
                      <ul class="icons alt">
                          <li>
                            <a href="#" class="icon alt fa-vk">
                              <span class="label">VK</span>
                            </a>
                          </li>
                          <li>
                            <a href="#" class="icon alt fa-instagram">
                              <span class="label">Instagram</span>
                            </a>
                          </li>
                      </ul>

                  </section>
                  <section class="colleagues">
                          <h4>Коллеги</h4>
                          <ul class="colleagues-list">
                              <li><a class="fed_archives" href="http://archives.ru" title="Федеральное архивное агентство"></a></li>
                              <li><a class="fed_archives_portal" href="http://www.rusarchives.ru" title="Портал архивы России"></a></li>
                              <li><a class="kirov_minkult" href="http://cultura.kirovreg.ru/" title="Министерство культуры Кировской области"></a></li>
                          </ul>
                  </section>
              </footer>
-->

<!--
              <div id="copyright">
                  <ul><li>&copy; 2019-2020 ЦГАКО</li><li>Дизайн: <a href="https://vk.com/goomba41">Бородавкин А.В.</a></li><li>Использование материалов сайта без согласования с КОГБУ ЦГАКО запрещено</li></ul>
              </div>
-->

          </div>

      </body>
  </html>

</template>

<script src="../assets/js/jquery.min.js"></script>
<script src="../assets/js/jquery.scrollex.min.js"></script>
<script src="../assets/js/jquery.scrolly.min.js"></script>
<script src="../assets/js/browser.min.js"></script>
<script src="../assets/js/breakpoints.min.js"></script>
<script src="../assets/js/util.js"></script>
<script src="../assets/js/main.js"></script>
<script src="../assets/js/to-top.js"></script>
<script src="../assets/js/anchors.js"></script>
<script src="../assets/js/search.js"></script>
<script src="../assets/js/underscore-min.js"></script>
<script src="../assets/js/moment-with-locales.js"></script>
<script src="../assets/js/clndr.js"></script>
<script src="../assets/js/slider.js"></script>
<script src="../assets/js/sticky-nav.js"></script>

<style lang="css">
@import '../assets/css/main.css';
@import '../assets/css/slider.css';
@import '../assets/css/noscript.css';
</style>

<script>
import { mapState } from 'vuex';
import NodeTree from './NodeTree';

export default {
  name: 'Index',
  data() {
    return {
    };
  },
  beforeMount() {
    this.$store.dispatch('loadStructure');
  },
  computed: mapState({
    menu: state => state.structure,
  }),
  components: {
    NodeTree
  },
};
</script>
