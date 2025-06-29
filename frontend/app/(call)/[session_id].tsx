import React, { useEffect } from "react";
import { View, Text, ActivityIndicator } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { LiveKitProvider } from "../../components/LiveKitProvider";
import { useLiveKit } from "../../hooks/useLiveKit";


 const CallScreen=()=> {
  const { session_id } = useLocalSearchParams<{ session_id: string }>();
  const { token, error, isLoading, getToken } = useLiveKit();
  const LIVEKIT_WS_URL = "wss://mindfull-4wx7pfsc.livekit.cloud";

  useEffect(() => {
    // Get LiveKit token when screen loads
    getToken(session_id, "user-123"); // Replace with actual user ID
  }, [session_id, getToken]);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
        <Text>Joining call...</Text>
      </View>
    );
  }

  if (error || !token) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <Text>Error joining call: {error}</Text>
      </View>
    );
  }

  return (
    <LiveKitProvider
      token={token}
      url={LIVEKIT_WS_URL}
      onConnected={() => console.log("Connected to LiveKit")}
      onDisconnected={() => console.log("Disconnected from LiveKit")}
    >
      <View style={{ flex: 1, backgroundColor: "#000" }}>
        <Text style={{ color: "white", textAlign: "center", marginTop: 50 }}>
          Call Session: {session_id}
        </Text>
        {/* Add your video components, controls, etc. here */}
        <View
          style={{ flex: 1, justifyContent: "center", alignItems: "center" }}
        >
          <Text style={{ color: "white" }}>
            Video call interface will go here
          </Text>
        </View>
      </View>
    </LiveKitProvider>
  );
}
export default CallScreen;