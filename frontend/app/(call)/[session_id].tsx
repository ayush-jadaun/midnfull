import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  ActivityIndicator,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
} from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import { useLiveKit } from "../../hooks/useLiveKit";

const { width } = Dimensions.get("window");


const COLORS = {
  background: "#1a1a1a",
  card: "#2a2a2a",
  primary: "#6C63FF",
  secondary: "#A3D9C9",
  accent: "#FF6B6B",
  success: "#00C851",
  error: "#FF6B6B",
  text: "#FFFFFF",
  textSecondary: "#cccccc",
  textMuted: "#888888",
};

export default function CallScreen() {
  const { session_id } = useLocalSearchParams<{ session_id: string }>();
  const { token, error, isLoading, getToken } = useLiveKit();
  const [isConnected, setIsConnected] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  // Animation for audio visualizer
  const pulseAnim = React.useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (session_id) {
      getToken(session_id, "user-123");
    }
  }, [session_id, getToken]);

  useEffect(() => {
    const pulseAnimation = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.2,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    );

    if (isConnected) {
      pulseAnimation.start();
    } else {
      pulseAnimation.stop();
    }

    return () => pulseAnimation.stop();
  }, [isConnected, pulseAnim]);

  const handleEndCall = () => {
    router.back();
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  if (isLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>
          Connecting to your mindful session...
        </Text>
      </View>
    );
  }

  if (error || !token) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorIcon}>⚠️</Text>
        <Text style={styles.errorText}>Unable to connect to session</Text>
        <Text style={styles.errorSubtext}>{error}</Text>
        <TouchableOpacity
          style={styles.retryButton}
          onPress={() => session_id && getToken(session_id, "user-123")}
        >
          <Text style={styles.retryButtonText}>Try Again</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.backButton} onPress={handleEndCall}>
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.sessionText}>Mindful Session</Text>
        <Text style={styles.sessionId}>{session_id}</Text>
      </View>

      {/* Audio Visualizer */}
      <View style={styles.audioContainer}>
        <Animated.View
          style={[
            styles.audioVisualizer,
            {
              transform: [{ scale: pulseAnim }],
            },
          ]}
        >
          <Text style={styles.audioIcon}>🎙️</Text>
        </Animated.View>

        <Text
          style={[
            styles.statusText,
            { color: isConnected ? COLORS.success : COLORS.textSecondary },
          ]}
        >
          {isConnected ? "Connected - Speak freely" : "Connecting..."}
        </Text>

        <Text style={styles.instructionText}>
          Take a deep breath and share what's on your mind
        </Text>
      </View>

      {/* Control Buttons */}
      <View style={styles.controlsContainer}>
        <TouchableOpacity
          style={[
            styles.controlButton,
            styles.muteButton,
            isMuted && styles.muteButtonActive,
          ]}
          onPress={toggleMute}
          activeOpacity={0.8}
        >
          <Text style={styles.controlButtonIcon}>{isMuted ? "🔇" : "🎙️"}</Text>
          <Text style={styles.controlButtonText}>
            {isMuted ? "Unmute" : "Mute"}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.controlButton, styles.endCallButton]}
          onPress={handleEndCall}
          activeOpacity={0.8}
        >
          <Text style={styles.controlButtonIcon}>📞</Text>
          <Text style={styles.controlButtonText}>End Call</Text>
        </TouchableOpacity>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          Your conversation is private and secure
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingHorizontal: 24,
  },
  centerContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: COLORS.background,
    paddingHorizontal: 24,
  },
  header: {
    paddingTop: 60,
    paddingBottom: 20,
    alignItems: "center",
  },
  sessionText: {
    color: COLORS.text,
    fontSize: 24,
    fontWeight: "600",
    marginBottom: 8,
  },
  sessionId: {
    color: COLORS.textMuted,
    fontSize: 14,
    fontWeight: "400",
  },
  audioContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 40,
  },
  audioVisualizer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: COLORS.card,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 30,
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  audioIcon: {
    fontSize: 48,
  },
  statusText: {
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 12,
  },
  instructionText: {
    color: COLORS.textSecondary,
    fontSize: 16,
    textAlign: "center",
    lineHeight: 24,
    paddingHorizontal: 20,
  },
  controlsContainer: {
    flexDirection: "row",
    justifyContent: "space-around",
    paddingVertical: 30,
  },
  controlButton: {
    alignItems: "center",
    padding: 16,
    borderRadius: 50,
    minWidth: 80,
  },
  muteButton: {
    backgroundColor: COLORS.card,
  },
  muteButtonActive: {
    backgroundColor: COLORS.accent,
  },
  endCallButton: {
    backgroundColor: COLORS.error,
  },
  controlButtonIcon: {
    fontSize: 24,
    marginBottom: 8,
  },
  controlButtonText: {
    color: COLORS.text,
    fontSize: 12,
    fontWeight: "500",
  },
  footer: {
    paddingBottom: 40,
    alignItems: "center",
  },
  footerText: {
    color: COLORS.textMuted,
    fontSize: 12,
    textAlign: "center",
  },
  loadingText: {
    color: COLORS.text,
    marginTop: 16,
    fontSize: 16,
    textAlign: "center",
  },
  errorIcon: {
    fontSize: 48,
    marginBottom: 16,
  },
  errorText: {
    color: COLORS.error,
    fontSize: 18,
    fontWeight: "600",
    textAlign: "center",
    marginBottom: 8,
  },
  errorSubtext: {
    color: COLORS.textSecondary,
    fontSize: 14,
    textAlign: "center",
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  retryButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 24,
    marginBottom: 12,
  },
  retryButtonText: {
    color: COLORS.text,
    fontSize: 16,
    fontWeight: "600",
  },
  backButton: {
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  backButtonText: {
    color: COLORS.textSecondary,
    fontSize: 16,
    fontWeight: "500",
  },
});
