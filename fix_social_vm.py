import re

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "r") as f:
    c = f.read()

target = """    private val _searchResults = MutableStateFlow<List<UserProfile>>(emptyList())
    val searchResults: StateFlow<List<UserProfile>> = _searchResults.asStateFlow()
"""

replacement = target + """    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
"""

c = c.replace(target, replacement)

target2 = """    private fun startListening() {
        stopListening()
        conversationJob = viewModelScope.launch {
            repo.getConversations().collect { convs ->
                _conversations.value = convs
            }
        }
        storiesJob = viewModelScope.launch {
            repo.getStories().collect { sts ->
                _stories.value = sts
            }
        }
    }"""

replacement2 = """    private fun startListening() {
        stopListening()
        conversationJob = viewModelScope.launch {
            repo.getConversations().collect { convs ->
                _conversations.value = convs
                _isLoading.value = false
            }
        }
        storiesJob = viewModelScope.launch {
            repo.getStories().collect { sts ->
                _stories.value = sts
            }
        }
    }"""

c = c.replace(target2, replacement2)

target3 = """    init {
        viewModelScope.launch {
            AuthRepository.currentUserFlow.collect { authUser ->
                if (authUser != null) {
                    _currentUser.value = UserProfile(
                        uid = authUser.uid,
                        username = authUser.username,
                        firstName = authUser.firstName,
                        lastName = authUser.lastName,
                        photoUrl = authUser.photoUrl,
                        isOnline = true,
                        isProfilePublic = authUser.isProfilePublic
                    )
                    startListening()
                } else {
                    _currentUser.value = null
                    _isLoading.value = false
                    stopListening()
                }
            }
        }
    }"""

c = c.replace(target3, target3)

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "w") as f:
    f.write(c)

