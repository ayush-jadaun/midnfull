import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
} from "react-native";
import { router } from "expo-router";

const { width } = Dimensions.get("window");

// Enhanced color palette for a mindful, calming experience
const COLORS = {
  background: "#E6F1F5", // soft blue
  card: "#FFFFFF",
  primary: "#6C63FF", // lavender
  secondary: "#A3D9C9", // mint green
  tertiary: "#FFB3BA", // soft pink for onboarding
  buttonText: "#FFFFFF",
  title: "#1A1B3D", // deeper blue
  subtitle: "#4F5D75",
  shadow: "#B6E0E5",
};

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Mindful</Text>
        <Text style={styles.subtitle}>
          Your daily companion for peace of mind
        </Text>
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={() => router.push("/login")}
          activeOpacity={0.85}
        >
          <Text style={styles.buttonText}>Log In</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={() => router.push("/signup")}
          activeOpacity={0.85}
        >
          <Text style={styles.buttonText}>Sign Up</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <TouchableOpacity
          style={styles.onboardingLink}
          onPress={() => router.push("/(onboarding)/step1")}
          activeOpacity={0.7}
        >
          <Text style={styles.onboardingText}>View Onboarding</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingHorizontal: 24,
    paddingTop: 80,
    paddingBottom: 60,
  },
  header: {
    flex: 0.4,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 42,
    fontWeight: "800",
    color: COLORS.title,
    marginBottom: 16,
    letterSpacing: 0.5,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 18,
    color: COLORS.subtitle,
    textAlign: "center",
    lineHeight: 26,
    opacity: 0.9,
  },
  buttonContainer: {
    flex: 0.4,
    justifyContent: "center",
    paddingHorizontal: 20,
  },
  button: {
    width: "100%",
    paddingVertical: 18,
    borderRadius: 28,
    alignItems: "center",
    marginBottom: 16,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    elevation: 4,
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
    shadowColor: COLORS.primary,
  },
  secondaryButton: {
    backgroundColor: COLORS.secondary,
    shadowColor: COLORS.secondary,
  },
  buttonText: {
    color: COLORS.buttonText,
    fontSize: 18,
    fontWeight: "600",
    letterSpacing: 0.5,
  },
  footer: {
    flex: 0.2,
    justifyContent: "flex-end",
    alignItems: "center",
  },
  onboardingLink: {
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  onboardingText: {
    color: COLORS.subtitle,
    fontSize: 16,
    fontWeight: "500",
    textDecorationLine: "underline",
    opacity: 0.8,
  },
});
