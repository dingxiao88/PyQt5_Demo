#include "awtk.h"
#include "base/assets_manager.h"
#ifndef WITH_FS_RES
#ifdef WITH_STB_IMAGE
#else
#endif /*WITH_STB_IMAGE*/
#ifdef WITH_VGCANVAS
#endif /*WITH_VGCANVAS*/
#ifdef WITH_TRUETYPE_FONT
#else /*WITH_TRUETYPE_FONT*/
#endif /*WITH_TRUETYPE_FONT*/
#endif /*WITH_FS_RES*/

ret_t assets_init(void) {
  assets_manager_t* am = assets_manager();
  assets_manager_set_theme(am, "default");

#ifdef WITH_FS_RES
  assets_manager_preload(am, ASSET_TYPE_FONT, "default");
  assets_manager_preload(am, ASSET_TYPE_STYLE, "default");
#else
#ifdef WITH_TRUETYPE_FONT
#else /*WITH_TRUETYPE_FONT*/
#endif /*WITH_TRUETYPE_FONT*/
#ifdef WITH_VGCANVAS
#endif /*WITH_VGCANVAS*/
#endif

  tk_init_assets();
  return RET_OK;
}
