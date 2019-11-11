<template>
  <main class="container-fluid d-flex flex-column">
    <breadcumbs></breadcumbs>

    <b-row class="pb-4 m-0 w-100 flex-grow-1 blocker"
    v-if="!can(user_perms, 'get', 'pages')">
      <b-col class="align-self-center text-center">
        <font-awesome-icon :icon="['fa', 'lock']" fixed-width size="10x"/>
      </b-col>
    </b-row>

    <b-row class="pb-4 m-0 w-100" v-if="can(user_perms, 'get', 'pages')">
      <b-col align-self="start" class="text-center" sm="8">
        <b-row class="justify-content-start align-middle align-items-center">
          <span class="text-info pr-3">
            {{ $tc('sitePages.counter', pages.count) }}
          </span>

          <b-button v-bind:title="$t('sitePages.tooltips.newButton')"
          v-b-tooltip.hover class="mr-1" size="sm" variant="success"
          v-b-modal.new-modal v-if="can(user_perms, 'post', 'pages')">
            <font-awesome-icon icon="plus" fixed-width />
          </b-button>
          <b-button v-else class="mr-1"
          size="sm" v-bind:title="$t('sitePages.tooltips.newButton')"
          v-b-tooltip.hover>
            <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
          </b-button>

          <b-dropdown size="sm" class="mr-1"
          v-bind:disabled="!selected.length"
          v-bind:class="!selected.length">
            <template slot="button-content">
              <font-awesome-icon icon="list" fixed-width />
            </template>
            <b-dropdown-item variant="danger" v-b-modal.delete-group-modal
            v-if="can(user_perms, 'delete', 'pages')">
              <font-awesome-icon icon="trash" fixed-width />
              {{ $t('sitePages.titles.groupActions.deleteButton') }}
            </b-dropdown-item>
            <b-dropdown-item variant="dark"
            v-else>
              <font-awesome-icon icon="lock" fixed-width />
              {{ $t('sitePages.titles.groupActions.deleteButton') }}
            </b-dropdown-item>
<!--
            <b-dropdown-item disabled>
              <font-awesome-icon icon="power-off" fixed-width />
              Отключить
            </b-dropdown-item>

            <b-dropdown-item disabled>
              <font-awesome-icon icon="key" fixed-width />
              Блокировать пароль
            </b-dropdown-item>
-->
          </b-dropdown>
        </b-row>
      </b-col>

<!--
      <b-col sm="4" class="text-center">
        <b-row class="justify-content-center align-middle align-items-center">
          <b-col>
            <b-input-group size="sm">
              <b-input-group-text slot="prepend">
                <font-awesome-icon :icon="['fa', 'search']" fixed-width />
              </b-input-group-text>
              <b-form-input type="search"
              title="Найти" v-b-tooltip.hover
              autocomplete="off"
              v-model="searchPhrase"
              v-on:input="searchByText(pages.results)"/>
            </b-input-group>
          </b-col>
        </b-row>
      </b-col>
-->

      <b-col sm="4" class="text-center">
        <b-row class="justify-content-end align-middle align-items-center">
          <b-col sm="4">
            <b-input-group :append="'/ ' + pages.pages" size="sm"
              v-bind:title="$t('sitePages.tooltips.pageNavigation')" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="pages.pages"
              autocomplete="off"
              v-model="listControl.page"
              v-on:input="listBegin(); listChange()"/>
            </b-input-group>
          </b-col>
          <b-col sm="4">
            <b-input-group :prepend="$t('sitePages.tooltips.pageShowCountTitle')" size="sm"
              v-bind:title="$t('sitePages.tooltips.pageShowCount')" v-b-tooltip.hover>
              <b-form-input type="number" min=1 :max="pages.count - listControl.start + 1"
              autocomplete="off"
              v-model="listControl.limit"
              v-on:input="listChange(); listControl.page = 1"/>
            </b-input-group>
          </b-col>
        </b-row>
      </b-col>

    </b-row>

    <div class="row p-3" v-if="can(user_perms, 'get', 'pages')">
      <table class="table table-hover td-align-middle">
        <thead>
          <tr class="text-center">
            <th scope="col">
              <b-form-checkbox v-model="selectAll" @change="select"></b-form-checkbox>
            </th>
            <th scope="col">{{ $t('sitePages.titles.cover') }}</th>
            <th scope="col">
              {{ $t('sitePages.titles.title') }}
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='title';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
              </th>
            <th scope="col">{{ $t('sitePages.titles.info') }}
            </th>
            <th scope="col">{{ $t('sitePages.titles.creation_date') }}
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='creation_date';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
            </th>
            <th scope="col">
              {{ $t('sitePages.titles.section') }}
              <font-awesome-icon icon="sort"
              fixed-width
              @click="listControl.orderBy.field='structure.title';
              listControl.orderBy.asc=!listControl.orderBy.asc"/>
            </th>
            <th scope="col">{{ $t('sitePages.titles.management') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="page in orderedList" v-bind:key="page.id">
            <td>
              <b-form-checkbox
                v-model="selected"
                :value="page.id"></b-form-checkbox>
            </td>
            <td>
              <div class="card-profile-image mx-auto">
                <div class="profile-image-overlay"
                v-b-tooltip.hover
                v-bind:title="$t('sitePages.tooltips.coverTitle')">
                  <div v-b-modal.cover-modal v-b-tooltip.hover
                  @click="selectPage(page.id)"
                  v-bind:title="$t('sitePages.tooltips.coverUpdate')">
                    <font-awesome-icon :icon="['fa', 'upload']" fixed-width />
                  </div>
                  <div v-if="page.cover" v-b-tooltip.hover
                  v-bind:title="$t('sitePages.tooltips.coverDelete')"
                  @click="deletePageCover(page.id)">
                    <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                  </div>
                </div>
                <img v-if="page.cover" :src="'/static/page_covers/'+page.cover"
                alt="Фотокарточка" class="profile-image">
                <b-img
                  v-else
                  blank
                  blank-color="#0b4fa6"
                  alt="Фотокарточка"
                  class="profile-image">
                </b-img>
              </div>
            </td>
            <td>
              {{page.title}}
              <br><b>/{{page.uri}}</b>
            </td>
            <td>
              <span
                v-b-tooltip.hover
                v-bind:title="$t('sitePages.tooltips.acessible')"
              >
                <font-awesome-icon
                  :icon="['fa', 'check-circle']"
                  fixed-width
                  :class="page.mainpage ? 'text-success' : 'text-danger'"
                />
              </span>
              <span
                v-b-tooltip.hover
                v-bind:title="$t('sitePages.tooltips.mainpage')"
              >
              <font-awesome-icon
                :icon="['fa', 'home']"
                fixed-width
                :class="page.available ? 'text-success' : 'text-danger'"
              />
              </span><br>
              <span
                class="pr-1"
                v-b-tooltip.hover
                v-bind:title="$t('sitePages.tooltips.filesCount')"
              >
                {{page.files.length}}
                <font-awesome-icon
                  :icon="['fa', 'file-alt']"
                  fixed-width
                />
              </span>
              <span
                v-b-tooltip.hover
                v-bind:title="$t('sitePages.tooltips.imagesCount')"
              >
                {{page.gallery.length}}
                <font-awesome-icon
                  :icon="['fa', 'images']"
                  fixed-width
                />
              </span>
            </td>
            <td
              v-bind:title="$options.filters.moment(page.creation_date, 'YYYY-MM-DD, HH:mm:ss')"
              v-b-tooltip.hover
            >
                {{$options.filters.moment(page.creation_date, 'from')}}
            </td>
            <td>
              {{page.structure.title}}
            </td>
            <td>
                <b-button size="sm" v-bind:title="$t('sitePages.tooltips.filesButton')"
                class="mb-1"
                v-if="can(user_perms, 'put', 'pages')"
                v-b-modal.files-modal
                v-b-tooltip.hover variant="info"
                @click="selectPage(page.id)"
                :disabled="!(can(user_perms, 'put', 'pages'))">
                  <font-awesome-icon :icon="['fa', 'file-alt']" fixed-width />
                </b-button>
                <b-button v-else
                class="mb-1"
                size="sm" v-bind:title="$t('sitePages.tooltips.editButton')"
                v-b-tooltip.hover>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>
                <b-button size="sm" v-bind:title="$t('sitePages.tooltips.imageButton')"
                class="mb-1"
                v-if="can(user_perms, 'put', 'pages')"
                v-b-tooltip.hover variant="info"
                 @click="selectPage(page.id)"
                :disabled="!(can(user_perms, 'put', 'pages'))">
                  <font-awesome-icon :icon="['fa', 'images']" fixed-width />
                </b-button>
                <b-button v-else
                class="mb-1"
                size="sm" v-bind:title="$t('sitePages.tooltips.editButton')"
                v-b-tooltip.hover>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>

                <br>

                <b-button size="sm" v-bind:title="$t('sitePages.tooltips.editButton')"
                class="mb-1"
                v-if="can(user_perms, 'put', 'pages')"
                v-b-tooltip.hover.bottom variant="primary"
                v-b-modal.edit-modal @click="selectPage(page.id)"
                :disabled="!(can(user_perms, 'put', 'pages'))">
                  <font-awesome-icon :icon="['fa', 'pencil-alt']" fixed-width />
                </b-button>
                <b-button v-else
                class="mb-1"
                size="sm" v-bind:title="$t('sitePages.tooltips.editButton')"
                v-b-tooltip.hover.bottom>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>

                <b-button v-if="can(user_perms, 'delete', 'pages')"
                size="sm" v-bind:title="$t('sitePages.tooltips.deleteButton')"
                class="mb-1"
                variant="danger" v-b-tooltip.hover.bottom
                @click="selectPage(page.id)"
                v-b-modal.delete-modal>
                  <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
                </b-button>
                <b-button v-else
                class="mb-1"
                size="sm" v-bind:title="$t('sitePages.tooltips.deleteButton')"
                v-b-tooltip.hover.bottom>
                  <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
                </b-button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <b-modal id="delete-modal"
            @show="deletePassphrase=''"
            @hidden="deletePassphrase=''"
            @close="deletePassphrase=''"
             v-bind:title="$t('sitePages.deleteModal.title')"
             v-b-tooltip.hover
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'delete', 'pages')">

      <b-form class="w-100" @submit.prevent="deletePage(page.id)">

        <b-form-group
        :description="$t('sitePages.deleteModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deletePassphrase.$model"
              v-bind:placeholder="$t('sitePages.deleteModal.confirmationField.placeholder')"
              :state="$v.deletePassphrase.$dirty ? !$v.deletePassphrase.$error : null"
              @input="$v.deletePassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('sitePages.deleteModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deletePassphrase.$anyDirty || $v.deletePassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
              {{$t('sitePages.deleteModal.description')}}
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="delete-group-modal"
            @show="deleteGroupPassphrase=''"
            @hidden="deleteGroupPassphrase=''"
            @close="deleteGroupPassphrase=''"
             v-bind:title="$t('sitePages.deleteGroupModal.title')"
             v-b-tooltip.hover
             hide-footer size="sm" centered
            :header-bg-variant="'danger'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'delete', 'pages')">

      <b-form class="w-100" @submit.prevent="deletePage(selected)">
        <b-form-group
        :description="$t('sitePages.deleteGroupModal.confirmationField.description')">
          <b-input-group>

            <b-form-input
              name="confirmation-passphrase"
              autofocus
              v-model="$v.deleteGroupPassphrase.$model"
              v-bind:placeholder="$t('sitePages.deleteGroupModal.confirmationField.placeholder')"
              :state="$v.deleteGroupPassphrase.$dirty ? !$v.deleteGroupPassphrase.$error : null"
              @input="$v.deleteGroupPassphrase.$touch()">
            </b-form-input>
          </b-input-group>

        </b-form-group>
        <b-button type="submit" block
        variant="danger" v-bind:title="$t('sitePages.deleteGroupModal.tooltips.deleteButton')"
        v-b-tooltip.hover
        :disabled="!$v.deleteGroupPassphrase.$anyDirty || $v.deleteGroupPassphrase.$invalid">
          <font-awesome-icon :icon="['fa', 'trash']" fixed-width />
        </b-button>

        <div class="row mx-auto pl-3 pr-3 pt-3 border-top">
          <span class="text-danger notation text-center">
              <font-awesome-icon :icon="['fa', 'exclamation-triangle']"
              size="1x" fixed-width />
              {{$t('sitePages.deleteGroupModal.description')}}
          </span>
        </div>

      </b-form>
    </b-modal>

    <b-modal id="new-modal"
      v-bind:title="$t('sitePages.formNew.formTitle')"
      hide-footer size="xl" centered
      :header-bg-variant="'success'"
      :header-text-variant="'light'"
      @hidden="onReset"
      v-if="can(user_perms, 'post', 'pages')"
    >

      <b-form class="w-100" @submit.prevent="onSubmitNewPage" @reset="onReset">

        <b-form-group>
          <b-form-input name="title"
            type="text"
            autofocus
            v-bind:placeholder="$t('sitePages.formNew.formFields.title.placeholder')"
            trim
            v-model="$v.newPage.title.$model"
            :state="$v.newPage.title.$dirty ? !$v.newPage.title.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          :state="$v.newPage.title.$dirty ? !$v.newPage.title.$error : null">
            <span v-if="!$v.newPage.title.required">
              {{$t('sitePages.formNew.formFields.title.errors.required')}}
            </span>
            <span v-if="!$v.newPage.title.minLength">
              {{$t('sitePages.formNew.formFields.title.errors.minLength')}}
            </span>
            <span v-if="!$v.newPage.title.maxLength">
              {{$t('sitePages.formNew.formFields.title.errors.maxLength')}}
            </span>
            <span v-if="!$v.newPage.title.alpha">
              {{$t('sitePages.formNew.formFields.title.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <b-form-textarea
            v-bind:placeholder="$t('sitePages.formNew.formFields.description.placeholder')"
            autocomplete="off"
            rows="2" max-rows="6" no-resize
            v-model="$v.newPage.description.$model" name="about_me"
            :state="$v.newPage.description.$dirty ? !$v.newPage.description.$error : null"
          >
          </b-form-textarea>

          <b-form-invalid-feedback
          :state="$v.newPage.description.$dirty ? !$v.newPage.description.$error : null">
            <span v-if="!$v.newPage.description.required">
              {{$t('sitePages.formNew.formFields.description.errors.required')}}
            </span>
            <span v-if="!$v.newPage.description.minLength">
              {{$t('sitePages.formNew.formFields.description.errors.minLength')}}
            </span>
            <span v-if="!$v.newPage.description.maxLength">
              {{$t('sitePages.formNew.formFields.description.errors.maxLength')}}
            </span>
            <span v-if="!$v.newPage.description.alpha">
              {{$t('sitePages.formNew.formFields.description.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-form-input
              name="uri"
              v-bind:placeholder="$t('sitePages.formNew.formFields.uri.placeholder')"
              :state="$v.newPage.uri.$dirty ? !$v.newPage.uri.$error : null"
              v-model="$v.newPage.uri.$model"
            >
            </b-form-input>
            <b-input-group-append>
              <b-button variant="outline-primary"
              v-bind:title="$t('sitePages.formNew.tooltips.newURIGen')" v-b-tooltip.hover
              @click="newPage.uri = shortIdGen(); $v.newPage.uri.$touch()"
            >
                <font-awesome-icon :icon="['fa', 'sync-alt']" fixed-width />
              </b-button>
            </b-input-group-append>
          </b-input-group>

          <b-form-invalid-feedback
          :state="$v.newPage.uri.$dirty ? !$v.newPage.uri.$error : null">
            <span v-if="!$v.newPage.uri.required">
              {{$t('sitePages.formNew.formFields.uri.errors.required')}}
            </span>
            <span v-if="!$v.newPage.uri.minLength">
              {{$t('sitePages.formNew.formFields.uri.errors.minLength')}}
            </span>
            <span v-if="!$v.newPage.uri.maxLength">
              {{$t('sitePages.formNew.formFields.uri.errors.maxLength')}}
            </span>
            <span v-if="!$v.newPage.uri.alpha">
              {{$t('sitePages.formNew.formFields.uri.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
          <b-form-text slot="description">
            <i18n path="sitePages.formNew.formFields.uri.description">
              <font-awesome-icon :icon="['fa', 'sync-alt']" fixed-width slot="key"/>
            </i18n>
          </b-form-text>
        </b-form-group>

        <b-form-group>
          <vue-editor
            v-model="$v.newPage.text.$model"
            :editor-toolbar="customToolbar"
            :placeholder="$t('sitePages.formNew.formFields.text.placeholder')"
          />
          <b-form-invalid-feedback
          :state="$v.newPage.text.$dirty ? !$v.newPage.text.$error : null">
            <span v-if="!$v.newPage.text.required">
              {{$t('sitePages.formNew.formFields.text.errors.required')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <multiselect v-model="$v.newPage.section.$model"
          @select="$v.newPage.section.$touch()"
          v-bind:placeholder="$t('sitePages.formNew.formFields.section.placeholder')"
          label="title" track-by="title" :hideSelected="true"
          :options="sectionsEnd" :multiple="false" :allowEmpty="false"
          :selectLabel="$t('sitePages.formNew.formFields.section.selectLabel')">
            <span slot="noResult">
              {{$t('sitePages.formNew.formFields.section.errors.search')}}
            </span>
          </multiselect>
          <b-form-text slot="description">
            {{$t('sitePages.formNew.formFields.section.description')}}
          </b-form-text>

          <b-form-invalid-feedback
          :state="$v.newPage.section.$dirty ? !$v.newPage.section.$error : null">
            <span v-if="!$v.newPage.section.required">
              {{$t('sitePages.formEdit.formFields.section.errors.required')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group :label="$t('sitePages.formNew.formFields.keywords.placeholder')">
          <multiselect v-model="$v.newPage.keywords.$model"
          v-bind:placeholder="$t('sitePages.formNew.formFields.keywords.placeholder')"
          :taggable="true" :multiple="true" :options="$v.newPage.keywords.$model"
          @tag="addKeyword(newPage.keywords, $event)" :allowEmpty="false" :closeOnSelect="false"
          :optionsLimit="5"
          :tag-placeholder="$t('sitePages.formNew.formFields.keywords.tagPlaceholder')"
          :selectedLabel="$t('sitePages.formNew.formFields.keywords.selectedLabel')"
          :deselectLabel="$t('sitePages.formNew.formFields.keywords.deselectLabel')">
            <span slot="noOptions">
              {{$t('sitePages.formNew.formFields.keywords.empty')}}
            </span>
          </multiselect>

          <b-form-invalid-feedback
          :state="$v.newPage.keywords.$dirty ? !$v.newPage.keywords.$error : null">
            <span v-if="!$v.newPage.keywords.required">
              {{$t('sitePages.formNew.formFields.keywords.errors.required')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-row>
          <b-col cols="2">
            <b-form-group>
              <b-form-checkbox
                name="available"
                switch size="md"
                v-model="$v.newPage.available.$model"
              >
                {{$t('sitePages.formNew.formFields.available.placeholder')}}
              </b-form-checkbox>
            </b-form-group>
          </b-col>
          <b-col cols="2">
            <b-form-group>
              <b-form-checkbox
                name="mainpage"
                switch size="md"
                v-model="$v.newPage.mainpage.$model"
              >
                {{$t('sitePages.formNew.formFields.mainpage.placeholder')}}
              </b-form-checkbox>
            </b-form-group>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <b-button type="submit" variant="success" block
              v-bind:title="$t('sitePages.formNew.tooltips.submitButton')" v-b-tooltip.hover
              :disabled="!$v.newPage.$anyDirty || $v.newPage.$invalid || formPending"
            >
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
          <b-col>
            <b-button type="reset" variant="danger" block
              v-bind:title="$t('sitePages.formNew.tooltips.clearButton')" v-b-tooltip.hover
              :disabled="!$v.newPage.$anyDirty || formPending"
            >
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'times']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

      </b-form>

    </b-modal>

    <b-modal id="edit-modal"
      v-bind:title="$t('sitePages.formEdit.formTitle')"
      hide-footer size="xl" centered
      :header-bg-variant="'primary'"
      :header-text-variant="'light'"
      @hidden="onResetEdit"
      v-if="can(user_perms, 'put', 'pages')"
    >

      <b-form class="w-100" @submit.prevent="onSubmitUpdatePage">

        <b-form-group>
          <b-form-input name="title"
            type="text"
            autofocus
            v-bind:placeholder="$t('sitePages.formEdit.formFields.title.placeholder')"
            trim
            v-model="$v.page.title.$model"
            :state="$v.page.title.$dirty ? !$v.page.title.$error : null"
          ></b-form-input>

          <b-form-invalid-feedback
          :state="$v.page.title.$dirty ? !$v.page.title.$error : null">
            <span v-if="!$v.page.title.required">
              {{$t('sitePages.formEdit.formFields.title.errors.required')}}
            </span>
            <span v-if="!$v.page.title.minLength">
              {{$t('sitePages.formEdit.formFields.title.errors.minLength')}}
            </span>
            <span v-if="!$v.page.title.maxLength">
              {{$t('sitePages.formEdit.formFields.title.errors.maxLength')}}
            </span>
            <span v-if="!$v.page.title.alpha">
              {{$t('sitePages.formEdit.formFields.title.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-form-group>
          <b-form-textarea
            v-bind:placeholder="$t('sitePages.formEdit.formFields.description.placeholder')"
            autocomplete="off"
            rows="2" max-rows="6" no-resize
            v-model="$v.page.seo_description.$model" name="about_me"
            :state="$v.page.seo_description.$dirty ? !$v.page.seo_description.$error : null"
          >
          </b-form-textarea>

          <b-form-invalid-feedback
          :state="$v.page.seo_description.$dirty ? !$v.page.seo_description.$error : null">
            <span v-if="!$v.page.seo_description.required">
              {{$t('sitePages.formEdit.formFields.description.errors.required')}}
            </span>
            <span v-if="!$v.page.seo_description.minLength">
              {{$t('sitePages.formEdit.formFields.description.errors.minLength')}}
            </span>
            <span v-if="!$v.page.seo_description.maxLength">
              {{$t('sitePages.formEdit.formFields.description.errors.maxLength')}}
            </span>
            <span v-if="!$v.page.seo_description.alpha">
              {{$t('sitePages.formEdit.formFields.description.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <b-input-group>
            <b-form-input
              name="uri"
              v-bind:placeholder="$t('sitePages.formEdit.formFields.uri.placeholder')"
              :state="$v.page.uri.$dirty ? !$v.page.uri.$error : null"
              v-model="$v.page.uri.$model"
            >
            </b-form-input>
            <b-input-group-append>
              <b-button variant="outline-primary"
              v-bind:title="$t('sitePages.formEdit.tooltips.newURIGen')" v-b-tooltip.hover
              @click="page.uri = shortIdGen(); $v.page.uri.$touch()"
            >
                <font-awesome-icon :icon="['fa', 'sync-alt']" fixed-width />
              </b-button>
            </b-input-group-append>
          </b-input-group>

          <b-form-invalid-feedback
          :state="$v.page.uri.$dirty ? !$v.page.uri.$error : null">
            <span v-if="!$v.page.uri.required">
              {{$t('sitePages.formEdit.formFields.uri.errors.required')}}
            </span>
            <span v-if="!$v.page.uri.minLength">
              {{$t('sitePages.formEdit.formFields.uri.errors.minLength')}}
            </span>
            <span v-if="!$v.page.uri.maxLength">
              {{$t('sitePages.formEdit.formFields.uri.errors.maxLength')}}
            </span>
            <span v-if="!$v.page.uri.alpha">
              {{$t('sitePages.formEdit.formFields.uri.errors.alpha')}}
            </span>
          </b-form-invalid-feedback>
          <b-form-text slot="description">
            <i18n path="sitePages.formEdit.formFields.uri.description">
              <font-awesome-icon :icon="['fa', 'sync-alt']" fixed-width slot="key"/>
            </i18n>
          </b-form-text>
        </b-form-group>

        <b-form-group>
          <vue-editor
            v-model="$v.page.text.$model"
            :editor-toolbar="customToolbar"
            :placeholder="$t('sitePages.formEdit.formFields.text.placeholder')"
          />
          <b-form-invalid-feedback
          :state="$v.page.text.$dirty ? !$v.page.text.$error : null">
            <span v-if="!$v.page.text.required">
              {{$t('sitePages.formEdit.formFields.text.errors.required')}}
            </span>
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <multiselect v-model="$v.page.structure.$model"
          v-bind:placeholder="$t('sitePages.formEdit.formFields.section.placeholder')"
          label="title" track-by="title" :hideSelected="true"
          :options="sectionsEnd" :multiple="false" :allowEmpty="false"
          :selectLabel="$t('sitePages.formEdit.formFields.section.selectLabel')">
            <span slot="noResult">
              {{$t('sitePages.formEdit.formFields.section.errors.search')}}
            </span>
          </multiselect>
          <b-form-text slot="description">
            {{$t('sitePages.formEdit.formFields.section.description')}}
          </b-form-text>
        </b-form-group>

        <b-form-group>

          <b-form-group :label="$t('sitePages.formEdit.formFields.keywords.placeholder')">
            <multiselect v-model="$v.page.seo_keywords.$model"
            v-bind:placeholder="$t('sitePages.formEdit.formFields.keywords.placeholder')"
            :taggable="true" :multiple="true" :options="$v.page.seo_keywords.$model"
            @tag="addKeyword(page.seo_keywords, $event)" :allowEmpty="false" :closeOnSelect="false"
            :optionsLimit="5"
            :tag-placeholder="$t('sitePages.formEdit.formFields.keywords.tagPlaceholder')"
            :selectedLabel="$t('sitePages.formEdit.formFields.keywords.selectedLabel')"
            :deselectLabel="$t('sitePages.formEdit.formFields.keywords.deselectLabel')">
              <span slot="noOptions">
                {{$t('sitePages.formEdit.formFields.keywords.empty')}}
              </span>
            </multiselect>
          </b-form-group>

          <b-form-invalid-feedback
          :state="$v.page.seo_keywords.$dirty ? !$v.page.seo_keywords.$error : null">
            <span v-if="!$v.page.seo_keywords.required">
              {{$t('sitePages.formEdit.formFields.keywords.errors.required')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-row>
          <b-col cols="2">
            <b-form-group>
              <b-form-checkbox
                name="available"
                switch size="md"
                v-model="$v.page.available.$model"
              >
                {{$t('sitePages.formEdit.formFields.available.placeholder')}}
              </b-form-checkbox>
            </b-form-group>
          </b-col>
          <b-col cols="2">
            <b-form-group>
              <b-form-checkbox
                name="mainpage"
                switch size="md"
                v-model="$v.page.mainpage.$model"
              >
                {{$t('sitePages.formEdit.formFields.mainpage.placeholder')}}
              </b-form-checkbox>
            </b-form-group>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <b-button type="submit" variant="primary" block
              v-bind:title="$t('sitePages.formEdit.tooltips.submitButton')" v-b-tooltip.hover
              :disabled="!$v.page.$anyDirty || $v.page.$invalid || formPending"
            >
              <font-awesome-icon v-if="!formPending"
              :icon="['fa', 'save']" fixed-width />
              <b-spinner small v-if="formPending"></b-spinner>
            </b-button>
          </b-col>
        </b-row>

      </b-form>

    </b-modal>

    <b-modal id="cover-modal"
            @hidden="onResetImage"
            @close="onResetImage"
            v-bind:title="$t('sitePages.formCover.formTitle')"
            hide-footer size="md" centered
            :header-bg-variant="'primary'"
            :header-text-variant="'light'"
            v-if="can(user_perms, 'put', 'pages')">

      <div class=" row w-100 mx-auto pb-3 justify-content-center align-items-center">
        <img v-if="coverUpdate.imageData"
        :src="coverUpdate.imageData"
        alt="Фотокарточка"
        class="profile-image-preview preview-md preview-square mr-4">
        <b-img
          v-else
          blank
          blank-color="#0b4fa6"
          alt="Фотокарточка"
          class="profile-image-preview preview-md preview-square mr-4"
        >
        </b-img>
        <img v-if="coverUpdate.imageData"
        :src="coverUpdate.imageData"
        alt="Фотокарточка"
        class="profile-image-preview preview-md mr-4">
        <b-img
          v-else
          blank
          blank-color="#0b4fa6"
          alt="Фотокарточка"
          class="profile-image-preview preview-md mr-4"
        >
        </b-img>
        <img v-if="coverUpdate.imageData"
        :src="coverUpdate.imageData"
        alt="Фотокарточка"
        class="profile-image-preview preview-sm mr-4">
        <b-img
          v-else
          blank
          blank-color="#0b4fa6"
          alt="Фотокарточка"
          class="profile-image-preview preview-sm mr-4"
        >
        </b-img>
      </div>

      <b-form class="w-100" @submit.prevent="onSubmitCover(page.id)">
        <b-form-group
        :description="$t('sitePages.formCover.formDescription')">

          <b-form-file
            ref="coverImageInput"
            @input="onSelectCoverImage"
            lang="ru"
            v-bind:placeholder="$t('sitePages.formCover.formFields.file.placeholder')"
            v-bind:browse-text="$t('sitePages.formCover.formFields.file.browseButton')"
            accept="image/jpeg, image/png, image/gif"
            :state="$v.coverUpdate.$dirty ? !$v.coverUpdate.$anyError : null"
          ></b-form-file>
          <b-form-invalid-feedback
          :state="$v.coverUpdate.$dirty ? !$v.coverUpdate.$anyError : null">
            <span v-if="!$v.coverUpdate.size.maxValue">
              {{$t('sitePages.formCover.formFields.file.errors.maxValue')}}
            </span>
            <span v-if="!$v.coverUpdate.type.isImage">
              {{$t('sitePages.formCover.formFields.file.errors.isImage')}}
            </span>
          </b-form-invalid-feedback>

        </b-form-group>

        <b-button class="mb-3" type="submit" block variant="primary"
        v-bind:title="$t('sitePages.formCover.saveButton')" v-b-tooltip.hover
        :disabled="!$v.coverUpdate.$anyDirty || $v.coverUpdate.$invalid || this.fileCover == null">
          <font-awesome-icon :icon="['fa', 'save']" fixed-width />
        </b-button>

        <div class="row mx-auto pt-3 border-top">
          <b-progress v-if="isActiveProgress" :max="100" show-progress animated class="w-100">
            <b-progress-bar :value="progressValue" variant="success"
            :label="`${((progressValue / progressMax) * 100).toFixed(2)}%`">
            </b-progress-bar>
            <b-progress-bar :value="preloadValue" variant="primary"
            :label="`${preloadValue.toFixed(2)}%`">
            </b-progress-bar>
          </b-progress>
        </div>
      </b-form>
    </b-modal>

    <b-modal
      id="files-modal"
      v-bind:title="$t('sitePages.formFiles.formTitle')"
      hide-footer size="md" centered
      :header-bg-variant="'info'"
      :header-text-variant="'light'"
      v-if="can(user_perms, 'put', 'pages')"
      @hidden="onResetFiles"
      @close="onResetFiles"
    >
      <b-card
        no-body
        class="mb-3"
        v-for="(file, fIndex) in page.files"
        v-bind:key="fIndex"
      >
        <b-card-header header-tag="header" class="p-0" role="tab">
          <b-button-group class="w-100">
            <b-button
              block
              v-b-toggle="'fileAccordion-' + fIndex"
              class="text-left"
              variant="info"
              v-bind:title="file.name"
              v-b-tooltip.hover
            >
              <font-awesome-icon icon="file-alt" fixed-width />
              {{(file.name.length &lt; 16) ? file.name : file.name.substr(0, 16) + '...'}}
              <i>({{file.size}}, {{file.extension}})</i>
            </b-button>
            <b-button
              variant="secondary"
              v-bind:title="$t('sitePages.formFiles.downloadButton')"
              :href="'/static/page_files/'+file.fname"
              v-b-tooltip.hover
            >
              <font-awesome-icon icon="download" fixed-width />
            </b-button>
            <b-button
              variant="danger"
              v-if="can(user_perms, 'put', 'pages')"
              v-bind:title="$t('sitePages.formFiles.deleteButton')"
              v-b-tooltip.hover
              @click="confirmFileDeletion({ 'pid':page.id, 'fid':file.fid }, fIndex)"
            >
              <font-awesome-icon icon="trash" fixed-width />
            </b-button>
            <b-button
              v-else
              v-bind:title="$t('sitePages.formFiles.deleteButton')"
              v-b-tooltip.hover
            >
              <font-awesome-icon :icon="['fa', 'lock']" fixed-width />
            </b-button>
          </b-button-group>
        </b-card-header>
        <b-collapse
          :id="`fileAccordion-${fIndex}`"
          accordion="file"
          role="tabpanel"
          @shown="selectedPageFile=file"
          @hide="selectedPageFile=null"
        >
          <b-list-group flush>
            <b-list-group-item>
              <b-form-group>
                <b-input-group class="mt-3">
                  <b-form-input
                    :type="'text'"
                    v-model="$v.selectedPageFile.name.$model"
                    v-bind:placeholder="$t('sitePages.formFiles.formFields.name.placeholder')"
                    :state="$v.selectedPageFile.$dirty ? !$v.selectedPageFile.$anyError : null"
                  >
                  </b-form-input>
                  <b-input-group-append>
                    <b-button variant="outline-primary"
                    @click="onSubmitUpdateFileData({ 'pid':page.id, 'fid':file.fid })"
                    :disabled="!$v.selectedPageFile.$anyDirty || $v.selectedPageFile.$invalid
                      || selectedPageFile == null"
                    >
                      <font-awesome-icon :icon="['fa', 'save']" fixed-width />
                    </b-button>
                  </b-input-group-append>
                </b-input-group>
                <b-form-invalid-feedback
                  :state="$v.selectedPageFile.$dirty ? !$v.selectedPageFile.$anyError : null"
                >
                  <span v-if="!$v.selectedPageFile.name.required">
                    {{$t('sitePages.formNew.formFields.description.errors.required')}}
                  </span>
                  <span v-if="!$v.selectedPageFile.name.minLength">
                    {{$t('sitePages.formNew.formFields.description.errors.minLength')}}
                  </span>
                  <span v-if="!$v.selectedPageFile.name.maxLength">
                    {{$t('sitePages.formNew.formFields.description.errors.maxLength')}}
                  </span>
                  <span v-if="!$v.selectedPageFile.name.alpha">
                    {{$t('sitePages.formNew.formFields.description.errors.alpha')}}
                  </span>
                </b-form-invalid-feedback>
              </b-form-group>
            </b-list-group-item>

          </b-list-group>
        </b-collapse>

      </b-card>

      <b-col class="p-0">
        <h3 class="mb-0 small">
            {{$t('sitePages.formFiles.saveButton')}}:
        </h3>
        <b-card no-body class="pt-3 mt-3">
          <b-list-group flush>
            <b-list-group-item class="flex-column align-items-start align-middle">
              <b-form class="w-100" @submit.prevent="onSubmitFiles(page.id)">
                <b-form-group
                :description="$t('sitePages.formFiles.formDescription')">

                  <b-form-file
                    ref="filesInput"
                    @input="onSelectFiles"
                    lang="ru"
                    multiple
                    :file-name-formatter="formatNames"
                    v-bind:placeholder="$t('sitePages.formFiles.formFields.file.placeholder')"
                    v-bind:browse-text="$t('sitePages.formFiles.formFields.file.browseButton')"
                    accept=".odt, .doc, .docx, .zip, .pdf"
                    :state="$v.filesUpdate.$dirty ? !$v.filesUpdate.$anyError : null"
                  ></b-form-file>

                  <b-form-invalid-feedback
                    :state="$v.filesUpdate.$dirty ? !$v.filesUpdate.$anyError : null"
                    v-if="$v.filesUpdate.$anyError"
                  >
                      {{$t('sitePages.formFiles.formFields.file.error')}}
                  </b-form-invalid-feedback>

                </b-form-group>

                <b-button class="mb-3" type="submit" block variant="info"
                v-bind:title="$t('sitePages.formFiles.saveButton')" v-b-tooltip.hover
                :disabled="!$v.filesUpdate.$anyDirty || $v.filesUpdate.$invalid
                  || this.pageFiles == null"
                >
                  <font-awesome-icon :icon="['fa', 'save']" fixed-width />
                </b-button>

                <b-row class="mx-auto pt-3 border-top" v-if="isActiveProgress">
                  <b-progress :max="100" show-progress animated class="w-100">
                    <b-progress-bar :value="progressValue" variant="success"
                    :label="`${((progressValue / progressMax) * 100).toFixed(2)}%`">
                    </b-progress-bar>
                    <b-progress-bar :value="preloadValue" variant="primary"
                    :label="`${preloadValue.toFixed(2)}%`">
                    </b-progress-bar>
                  </b-progress>
                </b-row>
              </b-form>

            </b-list-group-item>
          </b-list-group>
        </b-card>
      </b-col>

    </b-modal>

  </main>
</template>

<script>
import moment from 'moment';
import shortid from 'shortid';
import Multiselect from 'vue-multiselect';
import { mapState } from 'vuex';
import _ from 'lodash';
import { VueEditor } from 'vue2-editor';
import {
  required, sameAs, minLength, maxLength, maxValue,
} from 'vuelidate/lib/validators';
import Breadcumbs from './Breadcumbs';
import {
  can, EventBus, formatBytes,
} from '@/utils';
import { imageType, docsType } from '@/validators';

export default {
  name: 'Pages',
  data() {
    return {
      page: {},
      selectedPageFile: null,
      deletePassphrase: '',
      deleteGroupPassphrase: '',
      selected: [],
      selectAll: false,
      preloadValue: 0,
      isActiveProgress: false,
      listControl: {
        page: 1,
        start: 1,
        limit: 20,
        orderBy: {
          field: 'text',
          asc: true,
        },
      },
      customToolbar: [
        [{ header: [false, 1, 2, 3, 4, 5, 6] }],
        ['bold', 'italic', 'underline'],
        [
          { align: '' },
          { align: 'center' },
          { align: 'right' },
          { align: 'justify' },
        ],
        [{ script: 'sub' }, { script: 'super' }],
        [{ color: [] }, { background: [] }],
        [{ list: 'ordered' }, { list: 'bullet' }],
        [{ indent: '-1' }, { indent: '+1' }],
        ['blockquote', 'code-block'],
        ['link', 'video'],
        [{ direction: 'rtl' }],
        ['clean'],
      ],
      can,
      newPage: {
        title: '',
        text: '',
        uri: shortid.generate(),
        description: '',
        keywords: [
          'ЦГАКО',
          'Центральный государственный архив Кировской области',
          'Архив',
          'Киров',
          'Вятка',
          'История',
          'Документы',
        ],
        available: true,
        mainpage: true,
        section: '',
      },
      fileCover: null,
      coverUpdate: {
        type: '',
        size: 0,
        imageData: '',
      },
      pageFiles: null,
      filesUpdate: [],
    };
  },
  validations: {
    deletePassphrase: {
      required,
      sameAsURI: sameAs(function sameURI() {
        return this.page.uri;
      }),
    },
    deleteGroupPassphrase: {
      required,
      sameAsPassphrase: sameAs(function samePassphrase() {
        return this.$t('sitePages.deleteGroupModal.confirmationField.passphrase');
      }),
    },
    newPage: {
      title: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(100),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      text: {
        required,
      },
      uri: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(50),
        alpha: val => /^[a-zA-Z0-9-_]*$/i.test(val),
      },
      description: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(255),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      keywords: {
        required,
      },
      available: {
        required,
      },
      mainpage: {
        required,
      },
      section: {
        required,
      },
    },
    page: {
      title: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(100),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      text: {
        required,
      },
      uri: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(50),
        alpha: val => /^[a-zA-Z0-9-_]*$/i.test(val),
      },
      seo_description: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(255),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
      seo_keywords: {
        required,
      },
      available: {
        required,
      },
      mainpage: {
        required,
      },
      structure: {
        required,
      },
    },
    coverUpdate: {
      size: {
        maxValue: maxValue(2),
      },
      type: {
        isImage: imageType,
      },
    },
    filesUpdate: {
      $each: {
        size: {
          maxValue: maxValue(10),
        },
        type: {
          isFile: docsType,
        },
      },
    },
    selectedPageFile: {
      name: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(255),
        alpha: val => /^[а-яёa-zА-ЯЁA-Z0-9\s\W]*$/i.test(val),
      },
    },
  },
  components: {
    Breadcumbs, Multiselect, VueEditor,
  },
  computed: mapState({
    pages: state => state.pages,
    user_perms: state => state.user_perms,
    sectionsEnd: state => state.sectionsEnd,
    uid: state => state.uid,
    orderedList() {
      return _.orderBy(this.pages.results,
        this.listControl.orderBy.field,
        this.listControl.orderBy.asc ? 'asc' : 'desc');
    },
    progressValue: state => state.uploadProgress,
    progressMax: state => state.uploadProgressMax,
    formPending: state => state.formPending,
  }),
  watch: {
    user_perms() {
      if (can(this.user_perms, 'get', 'pages')) {
        this.$store.dispatch('loadPages', { start: this.listControl.start, limit: this.listControl.limit });
        this.$store.dispatch('loadSectionsEnd', {});
      }
    },
  },
  methods: {
    dateFormatter(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    formatNames(files) {
      if (files.length === 1) {
        return files[0].name;
      }
      return this.$tc('sitePages.counterFiles', files.length);
    },
    shortIdGen() {
      return shortid.generate();
    },
    addKeyword(list, tag) {
      list.push(tag);
    },
    select() {
      this.selected = [];
      if (!this.selectAll) {
        for (let i = 0; i < this.pages.results.length; i += 1) {
          this.selected.push(this.pages.results[i].id);
        }
      }
    },
    onReset(evt) {
      evt.preventDefault();
      this.$v.newPage.$reset();

      this.newPage = {
        title: '',
        text: '',
        uri: shortid.generate(),
        description: '',
        keywords: [
          'ЦГАКО',
          'Центральный государственный архив Кировской области',
          'Архив',
          'Киров',
          'Вятка',
          'История',
          'Документы',
        ],
        available: true,
        mainpage: true,
        section: '',
      };
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onResetEdit(evt) {
      evt.preventDefault();
      this.$v.page.$reset();
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    selectPage(id) {
      this.page = _.find(this.pages.results, { id });
    },
    deletePage(id) {
      if (Array.isArray(id)) {
        for (let i = 0; i < id.length; i += 1) {
          this.$store.dispatch('deletePage', { id: id[i] });
        }
      } else if (!Number.isNaN(id)) {
        this.$store.dispatch('deletePage', { id });
      }
    },
    onSubmitNewPage() {
      this.$v.newPage.$touch();

      if (!this.$v.newPage.$invalid) {
        this.$store.dispatch('newPage', this.newPage);
      }
    },
    async onSubmitUpdatePage() {
      this.$v.page.$touch();

      if (!this.$v.page.$invalid) {
        await this.$store.dispatch('updatePage', this.page);
        this.$v.page.$reset();
        EventBus.$emit('forceRerender');
      }
    },
    deletePageCover(id) {
      this.$store.dispatch('deletePageCover', id);
    },
    onSelectCoverImage() {
      const { files } = this.$refs.coverImageInput.$refs.input;
      if (files && files[0]) {
        this.coverUpdate.type = files[0].type;
        this.coverUpdate.size = formatBytes(files[0].size, 2, 2).number;
        this.$v.coverUpdate.$touch();

        if (!this.$v.coverUpdate.$invalid) {
          const reader = new FileReader();
          reader.onprogress = (e) => {
            if (e.lengthComputable) {
              this.isActiveProgress = true;
              this.preloadValue = Math.round((e.loaded / e.total) * 100);
            }
          };
          reader.onload = (e) => {
            this.coverUpdate.imageData = e.target.result;
            this.fileCover = files;
          };
          reader.readAsDataURL(files[0]);
          this.$emit('input', files[0]);
        }
      }
    },
    onResetImage(evt) {
      evt.preventDefault();
      this.page = {};
      this.fileCover = null;
      this.coverUpdate.type = '';
      this.coverUpdate.size = 0;
      this.coverUpdate.imageData = '';
      this.isActiveProgress = false;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onSubmitCover(id) {
      this.$v.coverUpdate.$touch();

      if (!this.$v.coverUpdate.$invalid) {
        const formData = new FormData();
        if (this.fileCover) {
          formData.append('cover', this.fileCover[0]);
        }
        this.isActiveProgress = true;
        this.$store.dispatch('updatePageCover', { formData, id });
      }
    },
    onSelectFiles() {
      const { files } = this.$refs.filesInput.$refs.input;
      this.filesUpdate = [];
      if (files && files[0]) {
        Array.from(files).forEach((file) => {
          this.filesUpdate.push({
            type: file.type,
            size: formatBytes(file.size, 2, 2).number,
            name: file.name,
          });
        });

        this.$v.filesUpdate.$touch();
        if (!this.$v.filesUpdate.$invalid) {
          this.pageFiles = files;
        }
      }
    },
    onResetFiles(evt) {
      evt.preventDefault();
      this.page = {};
      this.pageFiles = null;
      this.filesUpdate = [];
      this.isActiveProgress = false;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      EventBus.$emit('forceRerender');
    },
    onSubmitFiles(id) {
      this.$v.filesUpdate.$touch();
      if (!this.$v.filesUpdate.$invalid) {
        const formData = new FormData();
        if (this.pageFiles) {
          Array.from(this.pageFiles).forEach((f) => {
            formData.append('file[]', f);
          });
        }
        this.isActiveProgress = true;
        this.$store.dispatch('postPageFiles', { formData, id });
      }
    },
    confirmFileDeletion(ids, fIndex) {
      this.boxTwo = '';
      this.$bvModal.msgBoxConfirm(this.$t('sitePages.formFiles.deleteConfirm.description'), {
        title: this.$t('sitePages.formFiles.deleteConfirm.title'),
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: this.$t('sitePages.formFiles.deleteConfirm.yes'),
        cancelTitle: this.$t('sitePages.formFiles.deleteConfirm.no'),
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true,
      })
        .then((value) => {
          if (value) {
            this.$store.dispatch('deletePageFile', ids)
              .then(() => {
                this.page.files.splice(fIndex, 1);
              });
          }
        })
        .catch((err) => {
          EventBus.$emit('message', err);
        });
    },
    onSubmitUpdateFileData(ids) {
      this.$v.selectedPageFile.$touch();
      if (!this.$v.selectedPageFile.$invalid) {
        this.$store.dispatch('updatePageFileData', { ids, data: this.selectedPageFile });
        this.$v.selectedPageFile.$reset();
      }
    },
    listRows() {
      const newLimit = parseInt(parseInt(this.pages.count, 10)
      - parseInt(this.listControl.start, 10) + 1, 10);
      const limit = parseInt(this.listControl.limit, 10);
      if (limit > newLimit) {
        this.listControl.limit = newLimit;
      }
    },
    listBegin() {
      const newBegin = parseInt(parseInt(this.listControl.limit, 10)
      * parseInt(this.listControl.page, 10) - (parseInt(this.listControl.limit - 1, 10)), 10);
      if (newBegin > this.pages.count) {
        this.listControl.start = this.pages.count;
      } else {
        this.listControl.start = newBegin;
      }
    },
    listChange() {
      this.$store.dispatch('loadPages', { start: this.listControl.start, limit: this.listControl.limit });
    },
  },
};
</script>
