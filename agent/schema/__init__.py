# Schema is a separate module, this is one of the module created on
# the basis of functionality, rather than a feature. The reason is that
# we want to publish all schema in a separate package and maintain versions
# throughout features, and any change to schema in any feature should brake tests
# and a new version should be created every time. Although, we can put
# an argument that having schema in their own feature can also provide
# same functionality, however, if we move schema and features to separate repo
# then we won't have features in same folder and this argument may not apply.
