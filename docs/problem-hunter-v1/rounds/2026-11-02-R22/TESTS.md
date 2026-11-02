# R22 read-type contract

Actual vs required destination types in extract_weather_data, pinned a30374b045c138dac3f6dd4267ef8eb7390a7670:

|Field|Destination|Descriptor requires|
|---|---|---|
|WEATHER_TEMP|float|float|
|WEATHER_HUM|float|float|
|WEATHER_WIND_SPEED|float|float|
|WEATHER_WIND_GUST|float|float|
|WEATHER_WIND_DIR|float|uint16_t|
|WEATHER_SOLAR_RAD|float|float|
|WEATHER_UV_INDEX|uint8_t|uint8_t|
|WEATHER_PRECIP_RATE|float|float|
|WEATHER_PRESSURE|float|float|
|WEATHER_PRECIP_CML|float|float|

Host C++17, -O2, exit 0: 4 cases passed. No invalid typed dereference executed. Compile the following stubs and driver around the verbatim template definitions of ref_field_val, get_field_val and get_field_val_from_pack from the pinned ws_fields.h (in namespace WsFields). This checks extraction, not firmware layout, observation serialization, cardinal conversion or hardware. A disabled/absent direction and valid zero should be checked separately in an endpoint regression.

```cpp
#include <initializer_list>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdio>
namespace WsCommon {enum class RetRes {OK, ERROR_BAD_PARAMS, ERROR_NOT_SUPPORTED, ERROR_NOT_FOUND};}
namespace WsFields {enum class ValueType {FLOAT,U8,U16,U32,INT,BOOL};enum class FieldType{NONE,WEATHER_WIND_DIR};struct Desc{ValueType data_type;FieldType type;const char*name;};union Value{float val_float;uint8_t val_u8;uint16_t val_u16;uint32_t val_u32;int val_int;bool val_bool;};struct Field{Desc*info;Value value;WsCommon::RetRes decode_status;};struct FieldPack{int field_count;Field*fields;};

// Insert the three pinned accessor definitions here.

}
int main(){using namespace WsFields;using R=WsCommon::RetRes;Desc d{ValueType::U16,FieldType::WEATHER_WIND_DIR,"dir"};Field f{};f.info=&d;f.decode_status=R::OK;FieldPack p{1,&f};for(uint16_t deg:{0,151,359}){f.value.val_u16=deg;uint16_t out=1234;assert(get_field_val_from_pack(&p,d.type,nullptr,&out)==R::OK);assert(static_cast<float>(out)==deg);}uint16_t out=1234;p.field_count=0;assert(get_field_val_from_pack(&p,d.type,nullptr,&out)==R::ERROR_NOT_FOUND&&out==1234);puts("4 cases passed");}
```
