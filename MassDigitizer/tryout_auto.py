from autoSuggest_popup import AutoSuggest_popup

# pop = AutoSuggest_popup('storage', 29)
pop = AutoSuggest_popup('taxonname', 29)
# res = pop.autosuggest_gui('box')
pop.Show()
# print('in test module - res:::', type(res))
# collObj = pop

# if collObj.table == 'storage':
#     print(f"table: {collObj.table}, name: {collObj.name},"
#           f" id: {collObj.id}, fullname: {collObj.fullname}, collectionid: {collObj.collectionId}")
# else:
#     try:
#         print(f"name: {collObj.name}, fullname: {collObj.fullname}, id: {collObj.id}, parentfullname: {collObj.parentFullName}")
#     except AttributeError:
#         print(f"name: {collObj.name}, id: {collObj.id}, fullname: {collObj.fullname}")
# #